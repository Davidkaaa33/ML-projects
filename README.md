# Machine Learning Projects

[![Portfolio CI](https://github.com/Davidkaaa33/ML-projects/actions/workflows/ci.yml/badge.svg)](https://github.com/Davidkaaa33/ML-projects/actions/workflows/ci.yml)
[![RAG Retrieval Evaluation](https://github.com/Davidkaaa33/ML-projects/actions/workflows/rag-evaluation.yml/badge.svg)](https://github.com/Davidkaaa33/ML-projects/actions/workflows/rag-evaluation.yml)

End-to-end ML engineering portfolio covering tabular modeling, NLP, typo correction, APIs, Docker and local RAG.

**5 projects · tests in every project · 2 API services · reproducible evaluation artifacts · CI security/dependency audits**

> **Featured external project:** [Avito Candidate Retrieval](https://github.com/Davidkaaa33/avito-ds-bootcamp-2026-solution) — hybrid BM25 + BGE-M3 + geographic/microcategory retrieval with **Recall@50 0.831562**.

## Projects

| Project | Focus | Methods | Result |
| --- | --- | --- | --- |
| [Bank Transaction Fraud Detection](bank-transaction-fraud-detection/) | imbalanced classification | feature engineering · Logistic Regression · Random Forest · threshold tuning | ROC-AUC **0.8713** · PR-AUC **0.3399** |
| [Credit Repayment Prediction](credit-repayment-prediction/) | tabular risk | sklearn Pipeline · Logistic Regression · Random Forest | ROC-AUC **0.9550** · F1 **0.9162** |
| [SMS Spam Detector](spam-detector/) | NLP + serving | deduplication · TF-IDF · Multinomial NB · FastAPI · Docker | Precision **1.0000** · F1 **0.7642** |
| [T9 Typo Correction](T9-typo-correction/) | candidate ranking | Levenshtein search · explicit scoring · Random Forest | Top-1 **0.9775** · Top-3 **0.9982** |
| [LLM Knowledge Base Assistant](llm-knowledge-base-assistant/) | local RAG | SentenceTransformers · FAISS · Qwen/Ollama · FastAPI | Hit@1 **81.82%** · MRR@3 **0.9091** |

## What this repository demonstrates

- **Evaluation discipline** — baselines, validation design and held-out test sets before model complexity.
- **Leakage-safe ML** — preprocessing and model selection are kept inside reproducible pipelines.
- **Production-shaped interfaces** — FastAPI services, Docker images, health checks and container smoke tests.
- **RAG quality controls** — retrieval metrics, citation auditing, calibrated abstention and metric-drift checks.
- **Reproducibility** — pinned direct dependencies, committed machine-readable metrics and a pinned embedding-model revision.
- **Repository hygiene** — Ruff, tests, compilation checks and dependency vulnerability audits run in GitHub Actions.
- **Explicit limitations** — synthetic datasets, small evaluation sets and conditional metrics are documented rather than hidden.

## Where to start

For the strongest engineering example, open [LLM Knowledge Base Assistant](llm-knowledge-base-assistant/): it covers indexing, retrieval, evaluation, abstention, API serving and Docker.

For a compact deployable NLP service, open [SMS Spam Detector](spam-detector/). For classical ML workflow and validation design, start with [Credit Repayment Prediction](credit-repayment-prediction/) or [Bank Transaction Fraud Detection](bank-transaction-fraud-detection/).

## Reproduce the checks

Run the same core quality gates used in CI:

```bash
make install-tools
make install-classical
make install-rag
make check
```

RAG retrieval evaluation and abstention calibration can be run separately:

```bash
make rag-eval
make rag-calibrate
```

The tabular and T9 datasets are synthetic. The spam project uses the SMS Spam Collection dataset. Each project README documents its data assumptions, split design, metrics and limitations.
