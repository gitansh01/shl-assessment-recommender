from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple

import joblib
import numpy as np
from sentence_transformers import SentenceTransformer


@dataclass
class EmbeddingIndex:
    embeddings: np.ndarray
    item_ids: List[str]
    model_name: str
    model: SentenceTransformer | None = field(default=None, repr=False)

    def ensure_model(self) -> SentenceTransformer:
        if self.model is None:
            self.model = SentenceTransformer(self.model_name)
        return self.model

    def warmup(self) -> None:
        model = self.ensure_model()
        model.encode(["warmup"], normalize_embeddings=True)

    def search(self, query: str, k: int) -> List[Tuple[str, float]]:
        if not query.strip():
            return []
        model = self.ensure_model()
        query_vec = model.encode([query], normalize_embeddings=True)
        scores = np.dot(self.embeddings, query_vec[0])
        if scores.size == 0:
            return []
        ranked = np.argsort(scores)[::-1][:k]
        return [(self.item_ids[i], float(scores[i])) for i in ranked if scores[i] > 0]


def load_vector_index(index_path: str) -> Optional[EmbeddingIndex]:
    index_file = Path(index_path)
    if not index_file.exists():
        return None
    payload = joblib.load(index_file)
    embeddings = np.asarray(payload["embeddings"], dtype="float32")
    return EmbeddingIndex(
        embeddings=embeddings,
        item_ids=payload["item_ids"],
        model_name=payload["model_name"],
    )
