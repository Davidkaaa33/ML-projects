import numpy as np

from app.chunking import Chunk, chunk_document
from app.embeddings import EmbeddingModel
from app.ingestion import DATA_DIR, load_documents


def build_chunks() -> list[Chunk]:
    documents = load_documents(DATA_DIR)

    chunks = []

    for document in documents:
        chunks.extend(chunk_document(document))

    return chunks


def semantic_search(
    query: str,
    chunks: list[Chunk],
    embedding_model: EmbeddingModel,
    top_k: int = 3,
):
    chunk_embeddings = embedding_model.encode_chunks(chunks)

    query_embedding = embedding_model.encode_query(query)

    similarities = chunk_embeddings @ query_embedding

    best_indices = np.argsort(similarities)[::-1][:top_k]

    results = []

    for index in best_indices:
        results.append(
            {
                "chunk": chunks[index],
                "score": float(similarities[index]),
            }
        )

    return results


if __name__ == "__main__":
    chunks = build_chunks()

    embedding_model = EmbeddingModel()

    query = "How many vacation days do employees receive?"

    results = semantic_search(
        query=query,
        chunks=chunks,
        embedding_model=embedding_model,
        top_k=3,
    )

    print(f"\nQuery: {query}")

    for rank, result in enumerate(results, start=1):
        chunk = result["chunk"]
        score = result["score"]

        print("\n" + "=" * 60)
        print(f"Rank: {rank}")
        print(f"Score: {score:.4f}")
        print(f"Source: {chunk.source}")
        print(f"Chunk ID: {chunk.chunk_id}")
        print("-" * 60)
        print(chunk.text)
