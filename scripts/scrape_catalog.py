from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urljoin
import re

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

CATALOG_URL = "https://www.shl.com/products/product-catalog/"
LISTING_TYPE = "1"
EXCLUDE_KEYWORDS = [
    "solution",
    "job-focused-assessment",
    "job focused assessment",
    "short-form",
    "short form",
]


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def unique(items: List[str]) -> List[str]:
    seen = set()
    result = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result


def extract_list_page_links(html: str, base_url: str) -> List[str]:
    soup = BeautifulSoup(html, "lxml")
    links = []
    for anchor in soup.select("a[href]"):
        href = anchor.get("href", "")
        if "/products/product-catalog/" in href and "start=" in href and "type=" in href:
            if f"type={LISTING_TYPE}" in href:
                links.append(urljoin(base_url, href))
    return unique(links)


def extract_view_links(html: str, base_url: str) -> List[str]:
    soup = BeautifulSoup(html, "lxml")
    links = []
    for anchor in soup.select("a[href^='/products/product-catalog/view/']"):
        href = anchor.get("href", "")
        if href:
            links.append(urljoin(base_url, href))
    return unique(links)


def extract_section_value(soup: BeautifulSoup, label: str) -> str:
    header = soup.find(
        lambda tag: tag.name in {"h2", "h3", "h4"}
        and normalize_space(tag.get_text()).lower() == label.lower()
    )
    if not header:
        return ""
    text = normalize_space(header.parent.get_text(" "))
    if text.lower().startswith(label.lower()):
        return normalize_space(text[len(label) :])
    return text


def parse_test_type(container_text: str) -> str:
    match = re.search(
        r"Test Type:\s*([A-Z\s]+?)(?:Remote Testing:|Downloads|$)",
        container_text,
        re.S,
    )
    if not match:
        return ""
    letters = [letter for letter in re.findall(r"[A-Z]", match.group(1)) if letter.strip()]
    if not letters:
        return ""
    unique_letters = unique(letters)
    return " ".join(unique_letters)


def should_exclude(name: str, url: str, test_type: str) -> bool:
    combined = f"{name} {url}".lower()
    if any(keyword in combined for keyword in EXCLUDE_KEYWORDS):
        return True
    if test_type and len(test_type.split()) > 1:
        return True
    return False


def parse_product_page(html: str, url: str) -> Optional[dict]:
    soup = BeautifulSoup(html, "lxml")
    title_el = soup.find("h1")
    name = normalize_space(title_el.get_text()) if title_el else ""
    if not name:
        return None
    container = soup.select_one(".product-catalogue")
    container_text = (
        normalize_space(container.get_text("\n", strip=True)) if container else ""
    )
    description = extract_section_value(soup, "Description")
    if not description:
        description_el = soup.find("meta", {"name": "description"})
        description = normalize_space(description_el.get("content", "")) if description_el else ""

    job_levels = extract_section_value(soup, "Job levels")
    languages = extract_section_value(soup, "Languages")
    assessment_length = extract_section_value(soup, "Assessment length")
    test_type = parse_test_type(container_text)
    duration_minutes = None
    if assessment_length:
        match = re.search(r"(\d+)", assessment_length)
        if match:
            duration_minutes = int(match.group(1))

    if should_exclude(name, url, test_type):
        return None

    return {
        "id": normalize_space(url).lower().replace("https://", "").replace("http://", ""),
        "name": name,
        "url": url,
        "test_type": test_type,
        "description": description,
        "duration_minutes": duration_minutes,
        "job_family": [],
        "skills": [],
        "languages": [normalize_space(x) for x in languages.split(",") if normalize_space(x)],
        "job_levels": [normalize_space(x) for x in job_levels.split(",") if normalize_space(x)],
        "source": CATALOG_URL,
    }


def scrape_catalog(output_path: Path, limit: Optional[int], headless: bool) -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=headless)
        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            )
        )
        listing_url = f"{CATALOG_URL}?type={LISTING_TYPE}"
        page.goto(listing_url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(3000)
        html = page.content()
        list_pages = {listing_url, *extract_list_page_links(html, CATALOG_URL)}
        view_links: List[str] = []
        for list_page in sorted(list_pages):
            page.goto(list_page, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(2000)
            view_links.extend(extract_view_links(page.content(), CATALOG_URL))

        view_links = unique(view_links)
        if limit:
            view_links = view_links[:limit]

        items = []
        for link in view_links:
            page.goto(link, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(1500)
            item = parse_product_page(page.content(), link)
            if item:
                items.append(item)
        browser.close()

    payload = {
        "source": CATALOG_URL,
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "items": items,
    }
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape SHL product catalog.")
    parser.add_argument("--output", default="data/catalog.json")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--headless", action="store_true")
    args = parser.parse_args()
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    scrape_catalog(output_path, args.limit, args.headless)


if __name__ == "__main__":
    main()
