# ML Projects

A portfolio of machine learning projects covering tabular classification, imbalanced learning, feature engineering, model evaluation, NLP, and candidate ranking. Each project includes its dataset and a reproducible training or evaluation script.

| Project | Problem | Main methods | Result |
|---|---|---|---|
| [Bank Transaction Fraud Detection](bank-transaction-fraud-detection/) | Detect fraudulent transactions in imbalanced tabular data | Feature engineering, Logistic Regression, Random Forest, validation threshold tuning | Test ROC-AUC 0.8713, PR-AUC 0.3399, F1 0.3722 |
| [Credit Repayment Prediction](credit-repayment-prediction/) | Predict whether a credit will be repaid | One-hot encoding, Logistic Regression, Random Forest | Test ROC-AUC 0.9550, F1 0.9162 |
| [SMS Spam Detector](spam-detector/) | Classify SMS as spam or ham | TF-IDF, Multinomial Naive Bayes, FastAPI | Test precision 1.0000, recall 0.6183, F1 0.7642 |
| [T9 Typo Correction](T9-typo-correction/) | Generate and rank word corrections, then classify typo type | Edit distance, candidate scoring, Random Forest | Candidate top-1 accuracy 0.9775; conditional typo-type accuracy 1.0000 |

The tabular datasets and the T9 dataset are synthetic. The spam project uses the SMS Spam Collection dataset included in its project folder. See each project README for its validation design, limitations, and run commands.
