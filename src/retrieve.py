import pickle
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


INDEX_PATH = Path("data/index.faiss")
META_PATH = Path("data/meta.pkl")


class Retriever:
    def __init__(self):
        self.model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
        self.index = faiss.read_index(str(INDEX_PATH))
        with open(META_PATH, "rb") as f:
            self.documents = pickle.load(f)

    def search(self, query: str, top_k: int = 3):
        q = self.model.encode([query], convert_to_numpy=True, normalize_embeddings=True)
        q = q.astype(np.float32)

        scores, indices = self.index.search(q, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            results.append(
                {
                    "score": float(score),
                    "document": self.documents[idx],
                }
            )
        return results