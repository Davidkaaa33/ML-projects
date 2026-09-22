FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends libgomp1 && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY data/sample_docs ./data/sample_docs

# Build the FAISS index inside the image.
RUN python -m app.build_index

EXPOSE 8000

ENV OLLAMA_HOST=http://host.docker.internal:11434
ENV OLLAMA_MODEL=qwen3.5:4b

CMD ["python", "-m", "uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
