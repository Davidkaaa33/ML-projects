from app.chunking import Chunk


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


class EmbeddingModel:
    def __init__(self):
        # Keep model loading out of module import so API/unit tests can use
        # mocked assistants without downloading a transformer model.
        from sentence_transformers import SentenceTransformer

        self.model = SentenceTransformer(MODEL_NAME)

    def encode_chunks(self, chunks: list[Chunk]):
        texts = [chunk.text for chunk in chunks]

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
        )

        return embeddings

    def encode_query(self, query: str):
        embedding = self.model.encode(
            query,
            normalize_embeddings=True,
        )

        return embedding


if __name__ == "__main__":
    from app.ingestion import DATA_DIR, load_documents
    from app.chunking import chunk_document

    documents = load_documents(DATA_DIR)

    chunks = []

    for document in documents:
        chunks.extend(chunk_document(document))

    embedding_model = EmbeddingModel()

    embeddings = embedding_model.encode_chunks(chunks)

    print(f"Number of chunks: {len(chunks)}")
    print(f"Embeddings shape: {embeddings.shape}")

    print("\nFirst chunk:")
    print(chunks[0].text)

    print("\nFirst 10 embedding values:")
    print(embeddings[0][:10])
