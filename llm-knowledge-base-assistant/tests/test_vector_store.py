import numpy as np
import pytest

from app.chunking import Chunk
from app.vector_store import VectorStore


@pytest.fixture
def sample_store():
    chunks = [
        Chunk(
            text="Employees receive 28 vacation days.",
            source="policy.txt",
            chunk_id=0,
        ),
        Chunk(
            text="Technical support operates on business days.",
            source="support.txt",
            chunk_id=0,
        ),
    ]

    embeddings = np.array(
        [
            [1.0, 0.0],
            [0.0, 1.0],
        ],
        dtype=np.float32,
    )

    return VectorStore(embeddings, chunks)


def test_vector_search(sample_store):
    query = np.array(
        [1.0, 0.0],
        dtype=np.float32,
    )

    results = sample_store.search(
        query_embedding=query,
        top_k=2,
    )

    assert len(results) == 2

    assert results[0]["chunk"].source == "policy.txt"
    assert results[0]["score"] == pytest.approx(1.0)

    assert results[1]["chunk"].source == "support.txt"


def test_index_persistence(sample_store, tmp_path):
    index_path = tmp_path / "faiss.index"
    metadata_path = tmp_path / "chunks.json"

    sample_store.save(
        index_path=index_path,
        metadata_path=metadata_path,
    )

    assert index_path.exists()
    assert metadata_path.exists()

    loaded_store = VectorStore.load(
        index_path=index_path,
        metadata_path=metadata_path,
    )

    query = np.array(
        [1.0, 0.0],
        dtype=np.float32,
    )

    results = loaded_store.search(
        query_embedding=query,
        top_k=1,
    )

    assert results[0]["chunk"].source == "policy.txt"
    assert results[0]["chunk"].chunk_id == 0
