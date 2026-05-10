from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, List, Optional
import json
import re


def normalize_text(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", " ", value.lower())
    return re.sub(r"\s+", " ", normalized).strip()


@dataclass(frozen=True)
class Assessment:
    id: str
    name: str
    url: str
    test_type: str
    description: str = ""
    duration_minutes: Optional[int] = None
    job_family: List[str] = field(default_factory=list)
    job_levels: List[str] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    languages: List[str] = field(default_factory=list)
    source: str = ""

    @staticmethod
    def from_dict(data: dict) -> "Assessment":
        return Assessment(
            id=str(data.get("id") or "").strip(),
            name=str(data.get("name") or "").strip(),
            url=str(data.get("url") or "").strip(),
            test_type=str(data.get("test_type") or "").strip(),
            description=str(data.get("description") or "").strip(),
            duration_minutes=data.get("duration_minutes"),
            job_family=list(data.get("job_family") or []),
            job_levels=list(data.get("job_levels") or []),
            skills=list(data.get("skills") or []),
            languages=list(data.get("languages") or []),
            source=str(data.get("source") or "").strip(),
        )


class CatalogStore:
    def __init__(self, items: Iterable[Assessment]):
        self.items = list(items)
        self.by_id = {item.id: item for item in self.items if item.id}
        self.by_name = {normalize_text(item.name): item for item in self.items if item.name}

    def is_empty(self) -> bool:
        return not self.items

    def get_by_id(self, item_id: str) -> Optional[Assessment]:
        return self.by_id.get(item_id)

    def find_by_name(self, name: str) -> Optional[Assessment]:
        return self.by_name.get(normalize_text(name))

    def resolve_names(self, names: Iterable[str]) -> List[Assessment]:
        results: List[Assessment] = []
        seen = set()
        for name in names:
            normalized = normalize_text(name)
            if normalized in self.by_name:
                item = self.by_name[normalized]
                if item.id not in seen:
                    results.append(item)
                    seen.add(item.id)
                continue
            for key, item in self.by_name.items():
                if normalized and normalized in key and item.id not in seen:
                    results.append(item)
                    seen.add(item.id)
        return results

    def is_known_name(self, text: str) -> bool:
        normalized = normalize_text(text)
        if not normalized:
            return False
        for name in self.by_name:
            if name in normalized:
                return True
        return False

    def all_names(self) -> List[str]:
        return [item.name for item in self.items if item.name]


def load_catalog(path: str) -> CatalogStore:
    catalog_path = Path(path)
    if not catalog_path.exists():
        return CatalogStore([])
    raw = json.loads(catalog_path.read_text(encoding="utf-8"))
    items = raw.get("items", [])
    assessments = [Assessment.from_dict(item) for item in items if item]
    return CatalogStore(assessments)
