from pathlib import Path

from app.embeddings import EmbeddingModel
from app.vector_store import VectorStore


PROJECT_ROOT = Path(__file__).resolve().parents[1]

INDEX_DIR = PROJECT_ROOT / "data" / "index"

FAISS_PATH = INDEX_DIR / "faiss.index"
METADATA_PATH = INDEX_DIR / "chunks.json"


class Retriever:
    def __init__(self):
        self.embedding_model = EmbeddingModel()

        self.vector_store = VectorStore.load(
            index_path=FAISS_PATH,
            metadata_path=METADATA_PATH,
        )

    def retrieve(
        self,
        query: str,
        top_k: int = 3,
    ):
        query_embedding = self.embedding_model.encode_query(
            query
        )

        return self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )


if __name__ == "__main__":
    retriever = Retriever()

    query = (
        "What information should I provide "
        "when the AI service fails?"
    )

    results = retriever.retrieve(
        query=query,
        top_k=3,
    )

    print(f"\nQuery: {query}")

    for rank, result in enumerate(
        results,
        start=1,
    ):
        chunk = result["chunk"]

        print("\n" + "=" * 60)
        print(f"Rank: {rank}")
        print(f"Score: {result['score']:.4f}")
        print(f"Source: {chunk.source}")
        print(f"Chunk ID: {chunk.chunk_id}")
        print("-" * 60)
        print(chunk.text)
