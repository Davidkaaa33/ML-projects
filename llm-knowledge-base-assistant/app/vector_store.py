import json
from dataclasses import asdict
from pathlib import Path

import faiss
import numpy as np

from app.chunking import Chunk


class VectorStore:
    def __init__(
        self,
        embeddings: np.ndarray,
        chunks: list[Chunk],
    ):
        if len(embeddings) != len(chunks):
            raise ValueError(
                "Number of embeddings must match number of chunks"
            )

        embeddings = np.asarray(
            embeddings,
            dtype=np.float32,
        )

        self.chunks = chunks

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(embeddings)

    def search(
        self,
        query_embedding: np.ndarray,
        top_k: int = 3,
    ):
        query_embedding = np.asarray(
            query_embedding,
            dtype=np.float32,
        ).reshape(1, -1)

        top_k = min(top_k, len(self.chunks))

        scores, indices = self.index.search(
            query_embedding,
            top_k,
        )

        results = []

        for score, index in zip(scores[0], indices[0]):
            if index == -1:
                continue

            results.append(
                {
                    "chunk": self.chunks[index],
                    "score": float(score),
                }
            )

        return results

    def save(
        self,
        index_path: Path,
        metadata_path: Path,
    ):
        index_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        faiss.write_index(
            self.index,
            str(index_path),
        )

        metadata = [
            asdict(chunk)
            for chunk in self.chunks
        ]

        metadata_path.write_text(
            json.dumps(
                metadata,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    @classmethod
    def load(
        cls,
        index_path: Path,
        metadata_path: Path,
    ):
        index = faiss.read_index(
            str(index_path)
        )

        metadata = json.loads(
            metadata_path.read_text(
                encoding="utf-8"
            )
        )

        chunks = [
            Chunk(**item)
            for item in metadata
        ]

        store = cls.__new__(cls)

        store.index = index
        store.chunks = chunks

        return store
