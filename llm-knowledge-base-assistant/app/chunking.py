import re
from dataclasses import dataclass

from app.ingestion import Document


@dataclass
class Chunk:
    text: str
    source: str
    chunk_id: int


def split_into_sentences(text: str) -> list[str]:
    """
    Normalize whitespace and split text at sentence boundaries.
    """
    text = re.sub(r"\s+", " ", text).strip()

    sentences = re.split(r"(?<=[.!?])\s+", text)

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def chunk_document(
    document: Document,
    chunk_size: int = 250,
    overlap_sentences: int = 1,
) -> list[Chunk]:

    sentences = split_into_sentences(document.text)

    chunks = []
    current_sentences = []
    chunk_id = 0

    for sentence in sentences:
        candidate = " ".join(current_sentences + [sentence])

        if len(candidate) <= chunk_size or not current_sentences:
            current_sentences.append(sentence)
            continue

        chunk_text = " ".join(current_sentences)

        chunks.append(
            Chunk(
                text=chunk_text,
                source=document.source,
                chunk_id=chunk_id,
            )
        )

        chunk_id += 1

        if overlap_sentences > 0:
            current_sentences = current_sentences[-overlap_sentences:]
        else:
            current_sentences = []

        current_sentences.append(sentence)

    if current_sentences:
        chunk_text = " ".join(current_sentences)

        chunks.append(
            Chunk(
                text=chunk_text,
                source=document.source,
                chunk_id=chunk_id,
            )
        )

    return chunks


if __name__ == "__main__":
    from app.ingestion import DATA_DIR, load_documents

    documents = load_documents(DATA_DIR)

    for document in documents:
        chunks = chunk_document(document)

        print("\n" + "=" * 60)
        print(f"Document: {document.source}")
        print(f"Chunks: {len(chunks)}")
        print("=" * 60)

        for chunk in chunks:
            print(f"\nChunk {chunk.chunk_id}")
            print(chunk.text)
