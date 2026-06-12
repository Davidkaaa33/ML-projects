# T9 Advanced Typo Correction

A machine learning / NLP project that predicts the correct word given a misspelled word.  
The dataset focuses on **mistakes near the last letters** of words, mimicking common typing errors.

## Dataset

The dataset contains columns:

- `typo_word` — the misspelled word  
- `correct_word` — the intended correct word  
- `typo_type` — type of typo: `replace_last_letter`, `delete_last_letter`, `swap_last_two_letters`, `insert_near_ending`, `no_typo`  
- `mistake_position` — indicates which letters are affected (`last1`, `last2`, `last3`, `none`)  
- `edit_distance` — number of single-character edits to convert typo to correct word  
- `word_length` — length of the correct word  
- `typo_length` — length of the typo word  
- `length_difference` — `word_length - typo_length`  
- `same_first_letter` — 1 if the first letter matches, 0 otherwise  
- `is_last_letter_error` — 1 if the typo occurs in the last letters, 0 otherwise  

The dataset is saved in `data/t9_advanced_typo_correction_dataset.csv`.

## Technologies

- Python
- pandas
- numpy
- difflib (for initial similarity checking)
- Optional: python-Levenshtein for faster edit distance

## Project Steps

1. Load the dataset
2. Explore the data
3. Preprocess features for ML
4. Train a typo-correction model (using edit distance, T9 mapping, or ML classifier)
5. Predict corrected words for input sentences with typos
6. Evaluate the model with accuracy or top-k suggestions

## Status
In progress.

## Notes

- The dataset focuses on **last-letter mistakes** to simulate real typing errors.  
- This can be used for T9-style predictive text or typo-correction ML projects.
