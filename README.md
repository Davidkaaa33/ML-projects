# Machine Learning Projects

A compact portfolio of end-to-end ML work: tabular classification, imbalanced learning, NLP, typo correction and local Retrieval-Augmented Generation.

The emphasis is not on notebook screenshots. Each project has an explicit problem statement, a reproducible training/evaluation path, reported metrics, and a limitations section.

## Portfolio at a glance

| Project | Focus | Engineering / modeling angle | Reported result |
| --- | --- | --- | --- |
| [Bank Transaction Fraud Detection](bank-transaction-fraud-detection/) | Imbalanced tabular classification | feature engineering · sklearn Pipeline · validation threshold tuning | Test ROC-AUC **0.8713** · PR-AUC **0.3399** · F1 **0.3722** |
| [Credit Repayment Prediction](credit-repayment-prediction/) | Tabular risk prediction | leakage-safe preprocessing · Logistic Regression baseline · Random Forest | Test ROC-AUC **0.9550** · F1 **0.9162** |
| [SMS Spam Detector](spam-detector/) | Text classification + serving | deduplication before split · TF-IDF · Multinomial NB · FastAPI · Docker | Precision **1.0000** · Recall **0.6183** · F1 **0.7642** |
| [T9 Typo Correction](T9-typo-correction/) | Candidate generation + ranking | Levenshtein search · explicit ranking score · downstream typo-type classifier | Top-1 **0.9775** · Top-3 recall **0.9982** |
| [LLM Knowledge Base Assistant](llm-knowledge-base-assistant/) | Local RAG | SentenceTransformers · FAISS · Qwen/Ollama · FastAPI · tests · Docker | Hit@1 **81.82%** · Hit@3 **100%** · MRR@3 **0.9091** |

## What I optimize for

**Evaluation before complexity.** Baselines and validation design come before model sophistication. For imbalanced data, ranking and minority-class metrics are reported instead of hiding behind accuracy.

**Reproducible transformations.** Preprocessing is kept inside explicit pipelines or reusable modules so training and inference apply the same transformations.

**Held-out test discipline.** Where a validation split is used for model or threshold selection, the test split stays untouched until the decision is made.

**Operational shape.** Projects that benefit from serving include FastAPI/Docker paths rather than stopping at a training script.

**Limitations are part of the result.** Synthetic data, closed vocabularies, small evaluation sets and conditional metrics are documented instead of being presented as production guarantees.

## Project map

### 1. Bank Transaction Fraud Detection

Rare-event classification on an imbalanced synthetic transaction dataset. The project compares a prior-based dummy baseline, Logistic Regression and Random Forest, tunes the decision threshold on validation F1 and reports final ranking/classification metrics on an untouched test split.

→ [Open project](bank-transaction-fraud-detection/)

### 2. Credit Repayment Prediction

Structured credit-risk classification with categorical preprocessing inside an sklearn Pipeline. Logistic Regression provides the baseline; a small Random Forest search is selected by validation ROC-AUC before a single final test evaluation.

→ [Open project](credit-repayment-prediction/)

### 3. SMS Spam Detector

A small NLP service rather than only a classifier script: exact-message deduplication before splitting, TF-IDF + Multinomial Naive Bayes, serialized inference pipeline, FastAPI endpoint and Docker packaging.

→ [Open project](spam-detector/)

### 4. T9 Typo Correction

Separates **candidate ranking** from **typo-type classification**. Candidate generation uses edit distance over a known vocabulary, while the classifier receives only observable typo/candidate features.

→ [Open project](T9-typo-correction/)

### 5. LLM Knowledge Base Assistant

Local RAG over TXT/PDF documents with sentence-aware chunking, SentenceTransformer embeddings, FAISS retrieval and grounded generation through a locally hosted Qwen model via Ollama. Includes retrieval evaluation, citation auditing, API tests and Docker support.

→ [Open project](llm-knowledge-base-assistant/)

## Data notes

The tabular datasets and T9 dataset are synthetic. The spam project uses the SMS Spam Collection dataset included in its project folder. The RAG project ships its own evaluation questions and evaluation scripts.

For exact split design, model-selection logic, run commands and limitations, use the README inside each project directory.
