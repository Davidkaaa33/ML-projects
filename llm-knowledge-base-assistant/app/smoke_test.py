from app.rag import RAGAssistant


TEST_QUESTIONS = [
    "How many vacation days do employees receive?",
    "When is technical support available?",
    "What information should I provide when the AI service fails?",
    "Who is the company's CEO?",
]


def main():
    assistant = RAGAssistant()

    for question in TEST_QUESTIONS:
        print("\n" + "=" * 60)
        print(f"QUESTION: {question}")

        result = assistant.ask(
            question=question,
            top_k=3,
        )

        print(f"\nANSWER:\n{result['answer']}")

        print("\nRETRIEVED SOURCES:")

        for i, source in enumerate(
            result["retrieved_sources"],
            start=1,
        ):
            print(
                f"[{i}] {source['source']} "
                f"(chunk {source['chunk_id']}, "
                f"score={source['score']:.4f})"
            )


if __name__ == "__main__":
    main()
