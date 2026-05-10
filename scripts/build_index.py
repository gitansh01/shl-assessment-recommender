from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import List

import joblib
import numpy as np
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

from app.core.config import settings


def build_text(item: dict) -> str:
    parts = [
        item.get("name", ""),
        item.get("description", ""),
        f"Test type: {item.get('test_type', '')}",
        f"Skills: {', '.join(item.get('skills', []) or [])}",
        f"Job family: {', '.join(item.get('job_family', []) or [])}",
        f"Job levels: {', '.join(item.get('job_levels', []) or [])}",
    ]
    return "\n".join([part for part in parts if part])


def load_items(path: Path) -> List[dict]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return list(payload.get("items") or [])


def main() -> None:
    parser = argparse.ArgumentParser(description="Build embedding index for SHL catalog.")
    parser.add_argument("--catalog", default=settings.CATALOG_PATH)
    parser.add_argument("--index", default=settings.INDEX_PATH)
    args = parser.parse_args()

    catalog_path = Path(args.catalog)
    if not catalog_path.exists():
        raise FileNotFoundError(f"Catalog not found at {catalog_path}")

    items = load_items(catalog_path)
    if not items:
        raise ValueError("Catalog is empty.")

    texts = [build_text(item) for item in items]
    model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)
    embeddings = model.encode(
        texts,
        batch_size=32,
        normalize_embeddings=True,
        show_progress_bar=True,
    )
    embeddings = np.asarray(embeddings, dtype="float32")

    payload = {
        "embeddings": embeddings,
        "model_name": settings.EMBEDDING_MODEL_NAME,
        "item_ids": [str(item.get("id") or "") for item in items],
    }
    Path(args.index).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(payload, str(args.index))


if __name__ == "__main__":
    main()
