# T9 Typo Correction

A beginner-to-intermediate NLP and ML project for **correcting typos** and predicting the **type of typo** in words.

---

## Dataset

This project uses the **synthetic T9 typo correction dataset**.  

Columns:

- `typo_word` — the misspelled word  
- `correct_word` — the correct word  
- `typo_type` — type of typo: `replace_last_letter`, `delete_last_letter`, `swap_last_two_letters`, `insert_near_ending`, `no_typo`  
- `mistake_position` — where the typo occurs (`last1`, `last2`, `last3`, `none`)  
- `edit_distance` — number of edits between typo and correct word  
- `word_length` — length of the correct word  
- `typo_length` — length of the typo word  
- `length_difference` — difference between correct word length and typo length  
- `same_first_letter` — 1 if first letters match, 0 otherwise  
- `is_last_letter_error` — 1 if typo occurs in last letters, 0 otherwise  

Dataset file: `data/t9_advanced_typo_correction_dataset.csv`

---

## Technologies

- Python
- pandas
- numpy
- scikit-learn
- python-Levenshtein

---

## Project Steps

1. Load the dataset
2. Explore the data
3. Create features for words (edit distance, first letter match, last-letter error, etc.)
4. **Simple approach** — correct typos using Python `difflib`
5. **Advanced approach** — correct typos using Levenshtein distance and candidate scoring
6. **ML approach** — predict the type of typo using Random Forest classifier
7. Test custom words and sentences

---

## Metrics

For the ML approach:

- Accuracy
- Precision
- Recall
- F1-score
- Confusion matrix

---

## Status
Completed.

The project can:
- Correct typos in single words and full sentences
- Suggest multiple candidate corrections
- Predict the type of typo for ML-based analysis