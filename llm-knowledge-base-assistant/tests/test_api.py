from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from app import api as api_module


class FakeRAGAssistant:
    def __init__(self):
        self.retriever = SimpleNamespace(
            vector_store=SimpleNamespace(
                index=SimpleNamespace(ntotal=6)
            )
        )

    def ask(self, question: str, top_k: int = 3):
        return {
            "question": question,
            "answer": "Employees receive 28 vacation days.",
            "retrieved_sources": [
                {
                    "source": "company_policy.txt",
                    "chunk_id": 0,
                    "score": 0.8055,
                }
            ],
            "metrics": {
                "retrieval_seconds": 0.01,
                "generation_seconds": 0.20,
                "total_seconds": 0.21,
            },
        }


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(
        api_module,
        "RAGAssistant",
        FakeRAGAssistant,
    )

    with TestClient(api_module.app) as test_client:
        yield test_client


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "ready",
        "indexed_chunks": 6,
    }


def test_ask(client):
    response = client.post(
        "/ask",
        json={
            "question": "How many vacation days?",
            "top_k": 3,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "28 vacation days" in data["answer"]

    assert (
        data["retrieved_sources"][0]["source"]
        == "company_policy.txt"
    )

    assert "metrics" in data
    assert data["metrics"]["total_seconds"] == 0.21


def test_empty_question(client):
    response = client.post(
        "/ask",
        json={
            "question": "   ",
            "top_k": 3,
        },
    )

    assert response.status_code == 422
