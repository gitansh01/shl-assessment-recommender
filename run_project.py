#!/usr/bin/env python
"""Complete setup and run script for SHL Assessment Recommender."""

import subprocess
import sys
import time
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def run_command(cmd: str, description: str) -> bool:
    """Run a shell command and report status."""
    print(f"\n{'='*60}")
    print(f"[STEP] {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(cmd, shell=True, cwd=BASE_DIR)
        if result.returncode != 0:
            print(f"[ERROR] Failed: {description}")
            return False
        print(f"[OK] Success: {description}")
        return True
    except Exception as e:
        print(f"[ERROR] {e}")
        return False


def main():
    print("\n" + "="*60)
    print("SHL Assessment Recommender - Setup & Run")
    print("="*60)

    # Step 1: Install dependencies
    if not run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing Python dependencies"
    ):
        print("\n[ERROR] Setup failed at step 1")
        return

    # Step 2: Install Playwright browsers
    if not run_command(
        f"{sys.executable} -m playwright install",
        "Installing Playwright browsers"
    ):
        print("\n[WARN] Playwright install had issues, but continuing...")

    # Step 3: Create data directory
    data_dir = BASE_DIR / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    print(f"\n[OK] Data directory ready: {data_dir}")

    # Step 4: Scrape catalog (skip if already present unless forced)
    catalog_path = data_dir / "catalog.json"
    force_scrape = os.getenv("SHL_FORCE_SCRAPE", "").lower() in {"1", "true", "yes"}
    if catalog_path.exists() and catalog_path.stat().st_size > 0 and not force_scrape:
        print("\n[OK] Catalog already exists. Skipping scrape.")
        print("   To force re-scrape: set SHL_FORCE_SCRAPE=1 and re-run.")
    else:
        if not run_command(
            f"{sys.executable} scripts/scrape_catalog.py --headless",
            "Scraping SHL product catalog"
        ):
            print("\n[ERROR] Setup failed at step 4")
            return

    # Step 5: Build embedding index
    if not run_command(
        f"{sys.executable} scripts/build_index.py --catalog data/catalog.json --index data/index.pkl",
        "Building local embedding index"
    ):
        print("\n[ERROR] Setup failed at step 5")
        return

    # Step 6: Start API
    print(f"\n{'='*60}")
    print("Starting API server...")
    print(f"{'='*60}")
    print("\n[OK] Server starting at http://localhost:8000")
    print("[INFO] API docs at http://localhost:8000/docs")
    print("\n[TEST] /chat endpoint:")
    print("""
curl -X POST http://localhost:8000/chat ^
  -H "Content-Type: application/json" ^
  -d "{\\"messages\\":[{\\"role\\":\\"user\\",\\"content\\":\\"Hiring a Java developer\\"}]}"
""")
    print("\n[TEST] Health check:")
    print("curl http://localhost:8000/health\n")

    # Start the server
    run_command(
        f"{sys.executable} -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload",
        "Starting FastAPI server"
    )


if __name__ == "__main__":
    main()
