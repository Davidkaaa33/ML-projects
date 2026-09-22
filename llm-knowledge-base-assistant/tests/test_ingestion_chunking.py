from app.ingestion import Document, load_txt
from app.chunking import chunk_document


def test_load_txt(tmp_path):
    path = tmp_path / "sample.txt"
    path.write_text(
        "This is a test document.",
        encoding="utf-8",
    )

    document = load_txt(path)

    assert document.text == "This is a test document."
    assert document.source == "sample.txt"


def test_chunking_preserves_sentences():
    document = Document(
        text=(
            "Alpha one. "
            "Beta two. "
            "Gamma three. "
            "Delta four."
        ),
        source="sample.txt",
    )

    chunks = chunk_document(
        document,
        chunk_size=25,
        overlap_sentences=1,
    )

    assert len(chunks) == 3

    assert chunks[0].text == "Alpha one. Beta two."
    assert chunks[1].text == "Beta two. Gamma three."
    assert chunks[2].text == "Gamma three. Delta four."

    assert [chunk.chunk_id for chunk in chunks] == [0, 1, 2]

    assert all(
        chunk.source == "sample.txt"
        for chunk in chunks
    )
