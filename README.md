# Machine Learning Projects

[![Portfolio CI](https://github.com/Davidkaaa33/ML-projects/actions/workflows/ci.yml/badge.svg)](https://github.com/Davidkaaa33/ML-projects/actions/workflows/ci.yml)

A compact portfolio of end-to-end ML work across tabular modeling, NLP, typo correction and local RAG.

Each project includes a reproducible training/evaluation path, reported metrics and explicit limitations.

**5 projects · tests in every project · 2 API services · 1 local RAG system**

> **Featured external project:** [Avito Candidate Retrieval](https://github.com/Davidkaaa33/avito-ds-bootcamp-2026-solution) — hybrid BM25 + BGE-M3 + geographic/microcategory retrieval with **Recall@50 0.831562**.

| Project | Focus | Methods | Result |
| --- | --- | --- | --- |
| [Bank Transaction Fraud Detection](bank-transaction-fraud-detection/) | imbalanced classification | feature engineering · Logistic Regression · Random Forest · threshold tuning | ROC-AUC **0.8713** · PR-AUC **0.3399** |
| [Credit Repayment Prediction](credit-repayment-prediction/) | tabular risk | sklearn Pipeline · Logistic Regression · Random Forest | ROC-AUC **0.9550** · F1 **0.9162** |
| [SMS Spam Detector](spam-detector/) | NLP + serving | deduplication · TF-IDF · Multinomial NB · FastAPI · Docker | Precision **1.0000** · F1 **0.7642** |
| [T9 Typo Correction](T9-typo-correction/) | candidate ranking | Levenshtein search · explicit scoring · Random Forest | Top-1 **0.9775** · Top-3 **0.9982** |
| [LLM Knowledge Base Assistant](llm-knowledge-base-assistant/) | local RAG | SentenceTransformers · FAISS · Qwen/Ollama · FastAPI | Hit@1 **81.82%** · MRR@3 **0.9091** |

## Engineering principles

- **Evaluation before complexity** — baselines and validation design come first.
- **Leakage-safe preprocessing** — transformations live in pipelines or reusable modules.
- **Held-out test discipline** — test data is not used for model/threshold selection.
- **Operational shape** — serving-oriented projects include API/Docker paths.
- **Explicit limitations** — synthetic data, small eval sets and conditional metrics are called out.

The tabular and T9 datasets are synthetic. The spam project uses the SMS Spam Collection dataset. The RAG project includes its own retrieval evaluation and citation-audit tooling.

Open any project directory for the exact split design, implementation, run commands and limitations.

Run the portfolio quality gates locally with `make check`; the same core checks run automatically in GitHub Actions. Direct dependencies are pinned, Dependabot checks them weekly, and project metrics are committed as machine-readable artifacts where applicable.
