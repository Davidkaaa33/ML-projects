import time

from app.confidence import threshold_from_env
from app.llm import LLMClient
from app.retrieval import Retriever


ABSTENTION_ANSWER = "I don't know based on the provided documents."


class RAGAssistant:
    def __init__(
        self,
        retriever=None,
        llm=None,
        min_retrieval_score: float | None = None,
    ):
        self.retriever = retriever or Retriever()
        self.llm = llm or LLMClient()
        self.min_retrieval_score = (
            threshold_from_env()
            if min_retrieval_score is None
            else min_retrieval_score
        )

    @staticmethod
    def _sources(results):
        sources = []
        for result in results:
            chunk = result["chunk"]
            sources.append(
                {
                    "source": chunk.source,
                    "chunk_id": chunk.chunk_id,
                    "score": float(result["score"]),
                }
            )
        return sources

    def _abstain(
        self,
        question,
        sources,
        retrieval_seconds,
        total_start,
        reason,
        top_score,
    ):
        return {
            "question": question,
            "answer": ABSTENTION_ANSWER,
            "retrieved_sources": sources,
            "abstained": True,
            "abstention_reason": reason,
            "top_retrieval_score": top_score,
            "metrics": {
                "retrieval_seconds": round(retrieval_seconds, 4),
                "generation_seconds": 0.0,
                "total_seconds": round(time.perf_counter() - total_start, 4),
            },
        }

    def ask(
        self,
        question: str,
        top_k: int = 3,
    ) -> dict:
        total_start = time.perf_counter()
        retrieval_start = time.perf_counter()

        results = self.retriever.retrieve(
            query=question,
            top_k=top_k,
        )

        retrieval_seconds = time.perf_counter() - retrieval_start
        sources = self._sources(results)

        if not results:
            return self._abstain(
                question=question,
                sources=sources,
                retrieval_seconds=retrieval_seconds,
                total_start=total_start,
                reason="no_retrieval_results",
                top_score=None,
            )

        top_score = float(results[0]["score"])

        if (
            self.min_retrieval_score is not None
            and top_score < self.min_retrieval_score
        ):
            return self._abstain(
                question=question,
                sources=sources,
                retrieval_seconds=retrieval_seconds,
                total_start=total_start,
                reason="retrieval_score_below_threshold",
                top_score=top_score,
            )

        context_parts = []
        for i, result in enumerate(results, start=1):
            chunk = result["chunk"]
            context_parts.append(
                f"""[{i}] Source: {chunk.source}
Chunk ID: {chunk.chunk_id}

{chunk.text}"""
            )

        context = "\n\n---\n\n".join(context_parts)

        generation_start = time.perf_counter()
        answer = self.llm.generate_answer(
            question=question,
            context=context,
        )
        generation_seconds = time.perf_counter() - generation_start

        llm_abstained = (
            ABSTENTION_ANSWER.lower()
            in answer.lower()
        )

        return {
            "question": question,
            "answer": answer,
            "retrieved_sources": sources,
            "abstained": llm_abstained,
            "abstention_reason": "llm_abstention" if llm_abstained else None,
            "top_retrieval_score": top_score,
            "metrics": {
                "retrieval_seconds": round(retrieval_seconds, 4),
                "generation_seconds": round(generation_seconds, 4),
                "total_seconds": round(time.perf_counter() - total_start, 4),
            },
        }
