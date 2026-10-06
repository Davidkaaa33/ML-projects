from types import SimpleNamespace

from app.rag import ABSTENTION_ANSWER, RAGAssistant


class FakeRetriever:
    def __init__(self, results):
        self.results = results

    def retrieve(self, query, top_k=3):
        return self.results[:top_k]


class FakeLLM:
    def __init__(self, answer="Supported answer [1]."):
        self.answer = answer
        self.calls = 0

    def generate_answer(self, question, context):
        self.calls += 1
        return self.answer


def result(score=0.8):
    return {
        "chunk": SimpleNamespace(
            source="policy.txt",
            chunk_id=0,
            text="Employees receive 28 vacation days.",
        ),
        "score": score,
    }


def test_low_retrieval_score_abstains_without_llm_call():
    llm = FakeLLM()
    assistant = RAGAssistant(
        retriever=FakeRetriever([result(0.2)]),
        llm=llm,
        min_retrieval_score=0.5,
    )

    response = assistant.ask("Unsupported question")

    assert response["abstained"] is True
    assert response["answer"] == ABSTENTION_ANSWER
    assert response["abstention_reason"] == "retrieval_score_below_threshold"
    assert response["top_retrieval_score"] == 0.2
    assert response["metrics"]["generation_seconds"] == 0.0
    assert llm.calls == 0


def test_high_retrieval_score_calls_llm():
    llm = FakeLLM()
    assistant = RAGAssistant(
        retriever=FakeRetriever([result(0.8)]),
        llm=llm,
        min_retrieval_score=0.5,
    )

    response = assistant.ask("How many vacation days?")

    assert response["abstained"] is False
    assert response["abstention_reason"] is None
    assert response["top_retrieval_score"] == 0.8
    assert response["retrieved_sources"][0]["source"] == "policy.txt"
    assert llm.calls == 1


def test_empty_retrieval_abstains():
    llm = FakeLLM()
    assistant = RAGAssistant(
        retriever=FakeRetriever([]),
        llm=llm,
        min_retrieval_score=0.5,
    )

    response = assistant.ask("Anything")

    assert response["abstained"] is True
    assert response["abstention_reason"] == "no_retrieval_results"
    assert response["top_retrieval_score"] is None
    assert llm.calls == 0
