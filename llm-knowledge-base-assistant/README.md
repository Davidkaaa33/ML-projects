# LLM Knowledge Base Assistant

A local Retrieval-Augmented Generation (RAG) service for answering questions using internal documents.

The system retrieves relevant document chunks using SentenceTransformers and FAISS, then generates a grounded answer with a locally hosted Qwen model through Ollama.

No paid LLM API is required.

## Architecture

```mermaid
flowchart TD
    A[TXT / PDF Documents] --> B[Document Ingestion]
    B --> C[Sentence-aware Chunking]
    C --> D[SentenceTransformer Embeddings]
    D --> E[FAISS Vector Index]

    Q[User Question] --> F[Query Embedding]
    F --> E
    E --> G[Top-K Relevant Chunks]
    G --> H[Prompt + Retrieved Context]
    H --> I[Qwen 3.5 4B via Ollama]
    I --> J[Grounded Answer + Citations]
