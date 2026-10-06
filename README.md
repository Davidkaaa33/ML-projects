# Machine Learning Projects

[![Portfolio CI](https://github.com/Davidkaaa33/ML-projects/actions/workflows/ci.yml/badge.svg)](https://github.com/Davidkaaa33/ML-projects/actions/workflows/ci.yml)
[![RAG Retrieval Evaluation](https://github.com/Davidkaaa33/ML-projects/actions/workflows/rag-evaluation.yml/badge.svg)](https://github.com/Davidkaaa33/ML-projects/actions/workflows/rag-evaluation.yml)

## ML Systems Lab

**Five independently evaluated ML systems presented as one end-to-end product.**

The repository combines classical ML, NLP and local RAG with a recruiter-facing web interface, a unified FastAPI inference layer, Docker, tests, CI and committed evaluation artifacts. The interface is intentionally restrained: benchmark claims stay separate from interactive demo behavior.

```text
React / Vite
     │
     ▼
Unified FastAPI
     │
     ├── Transaction Risk ── sklearn pipeline
     ├── Credit Repayment ── sklearn pipeline
     ├── SMS Spam ────────── serialized TF-IDF + NB
     ├── T9 Correction ───── candidate ranking
     └── Knowledge Assistant ── optional FAISS + Qwen/Ollama service
```

### Run the product

The standard stack exposes four live demos plus reproducible RAG evaluation:

```bash
docker compose up --build
```

Open **http://localhost:8080**.

For live RAG generation, start Ollama on the host, make `qwen3.5:4b` available, then run:

```bash
docker compose --profile rag up --build
```

The heavy RAG runtime is optional by design. Without it, the site still exposes committed retrieval metrics and abstention calibration instead of pretending generation is available.

## Systems

| System | What it demonstrates | Result |
| --- | --- | --- |
| [Transaction Risk](bank-transaction-fraud-detection/) | imbalanced classification · feature engineering · threshold tuning | ROC-AUC **0.8713** · PR-AUC **0.3399** |
| [Credit Repayment](credit-repayment-prediction/) | leakage-safe preprocessing · validation-led model selection | ROC-AUC **0.9550** · F1 **0.9162** |
| [SMS Spam](spam-detector/) | deduplication · TF-IDF · FastAPI · Docker | Precision **1.0000** · F1 **0.7642** |
| [T9 Correction](T9-typo-correction/) | edit-distance retrieval · deterministic candidate ranking | Top-1 **0.9775** · Top-3 **0.9982** |
| [Knowledge Assistant](llm-knowledge-base-assistant/) | FAISS retrieval · citations · calibrated abstention · local LLM | Hit@1 **81.82%** · Hit@3 **100%** · MRR@3 **0.9091** |

> **External flagship:** [Avito Candidate Retrieval](https://github.com/Davidkaaa33/avito-ds-bootcamp-2026-solution) — hybrid BM25 + BGE-M3 + geographic/microcategory retrieval with **Recall@50 0.831562**.

## Product boundary

The web application does not reimplement the models. `apps/api` adapts the existing project code behind typed HTTP contracts:

- **Spam** loads the committed `model.joblib` artifact.
- **T9** calls the evaluated candidate-ranking implementation directly.
- **Fraud/Credit** lazily fit one interactive demo model using the already selected configuration and the full synthetic dataset.
- **Held-out benchmark metrics never come from those demo fits**; they remain sourced from committed evaluation artifacts.
- **RAG** stays a separate optional service because its embedding/index/LLM runtime is materially heavier than the other systems.

This separation keeps the demo useful without blurring evaluation methodology.

## Engineering evidence

| Area | Evidence |
| --- | --- |
| **Evaluation** | held-out metrics · JSON snapshots · RAG retrieval/calibration workflow |
| **Quality** | Ruff · pytest · compile checks · API contract tests |
| **Serving** | unified FastAPI gateway · project API services · health endpoints |
| **Containers** | non-root runtime containers · health checks · full-stack Compose |
| **RAG controls** | pinned embedding revision · abstention calibration · semantic metric-drift gate |
| **Security hygiene** | pinned direct dependencies · `pip-audit` in CI |
| **Reproducibility** | Python 3.12 · deterministic splits · committed metrics · one-command local stack |

## Repository map

```text
apps/
├── api/                         unified inference + model registry
└── web/                         recruiter-facing React interface

bank-transaction-fraud-detection/
credit-repayment-prediction/
spam-detector/
T9-typo-correction/
llm-knowledge-base-assistant/

scripts/                         repository-level validation
.github/workflows/               CI + RAG evaluation
docker-compose.yml               full product stack
Makefile                         local quality/evaluation commands
```

## Local quality gates

Install the lightweight dependencies required for repository checks:

```bash
make install-check
make check
```

Install the full embedding runtime only when reproducing RAG retrieval:

```bash
make install-rag
make rag-verify
```

`make rag-verify` rebuilds the FAISS index, recomputes retrieval and abstention metrics, then compares them with the committed snapshots using a small numerical tolerance.

## Data and limitations

The Fraud, Credit and T9 datasets are synthetic and are labeled as such in both the UI and project documentation. The Spam project uses the SMS Spam Collection dataset. The RAG evaluation corpus is intentionally small, so its calibrated abstention threshold is **measured but not silently enabled as a production default**.

For split design, feature logic, metric interpretation and model-specific limitations, use the README inside each project directory.
