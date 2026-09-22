import time

from app.llm import LLMClient
from app.retrieval import Retriever


class RAGAssistant:
    def __init__(self):
        self.retriever = Retriever()
        self.llm = LLMClient()

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

        retrieval_seconds = (
            time.perf_counter() - retrieval_start
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

        generation_seconds = (
            time.perf_counter() - generation_start
        )

        sources = []

        for result in results:
            chunk = result["chunk"]

            sources.append({
                "source": chunk.source,
                "chunk_id": chunk.chunk_id,
                "score": result["score"],
            })

        total_seconds = (
            time.perf_counter() - total_start
        )

        return {
            "question": question,
            "answer": answer,
            "retrieved_sources": sources,
            "metrics": {
                "retrieval_seconds": round(
                    retrieval_seconds,
                    4,
                ),
                "generation_seconds": round(
                    generation_seconds,
                    4,
                ),
                "total_seconds": round(
                    total_seconds,
                    4,
                ),
            },
        }
