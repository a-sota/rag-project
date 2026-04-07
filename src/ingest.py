import json
import pickle
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


DATA_PATH = Path("data/rag_qa.json")
INDEX_PATH = Path("data/index.faiss")
META_PATH = Path("data/meta.pkl")


def load_documents():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        rows = json.load(f)

    documents = []
    for row in rows:
        text = f"Q: {row['question']}\nA: {row['answer']}"
        documents.append(
            {
                "id": row["id"],
                "text": text,
                "question": row["question"],
                "answer": row["answer"],
            }
        )
    return documents


def main():
    model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    documents = load_documents()

    texts = [doc["text"] for doc in documents]
    embeddings = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    embeddings = embeddings.astype(np.float32)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)

    faiss.write_index(index, str(INDEX_PATH))
    with open(META_PATH, "wb") as f:
        pickle.dump(documents, f)

    print(f"Indexed {len(documents)} documents.")


if __name__ == "__main__":
    main()