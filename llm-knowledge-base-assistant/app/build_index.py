from pathlib import Path

from app.chunking import chunk_document
from app.embeddings import EmbeddingModel
from app.ingestion import DATA_DIR, load_documents
from app.vector_store import VectorStore


PROJECT_ROOT = Path(__file__).resolve().parents[1]

INDEX_DIR = PROJECT_ROOT / "data" / "index"

FAISS_PATH = INDEX_DIR / "faiss.index"
METADATA_PATH = INDEX_DIR / "chunks.json"


def build_index():
    documents = load_documents(DATA_DIR)

    chunks = []

    for document in documents:
        chunks.extend(
            chunk_document(document)
        )

    print(f"Documents loaded: {len(documents)}")
    print(f"Chunks created: {len(chunks)}")

    embedding_model = EmbeddingModel()

    embeddings = embedding_model.encode_chunks(
        chunks
    )

    vector_store = VectorStore(
        embeddings=embeddings,
        chunks=chunks,
    )

    vector_store.save(
        index_path=FAISS_PATH,
        metadata_path=METADATA_PATH,
    )

    print(f"FAISS index saved to: {FAISS_PATH}")
    print(f"Chunk metadata saved to: {METADATA_PATH}")


if __name__ == "__main__":
    build_index()
