# T9 Typo Correction

This project separates correction candidate ranking from typo-type classification.

## Dataset

The included synthetic dataset is `data/t9_typo_correction_dataset.csv` with 1,647 typo/correction pairs. It contains five typo types: replacement, deletion, insertion near the ending, last-two-letter swap, and no typo.

## Inference sequence

```text
raw typo
-> candidate generation from the known vocabulary
-> edit-distance candidate ranking
-> selected correction candidate
-> typo/candidate feature extraction
-> typo type classification
```

`simple_typo_corrector.py` provides a `difflib` baseline. `advanced_typo_corrector.py` filters by first letter and Levenshtein distance, then ranks candidates with a small explicit score. `typo_type_classifier.py` runs only after a candidate has been selected.

The classifier's features—edit distance, candidate and typo lengths, length difference, and first-letter match—are computed from the observed typo and selected candidate. It no longer reads the dataset's precomputed ground-truth-relative fields during inference.

## Results

Running candidate ranking on all 1,647 dataset rows gives:

| Metric | Value |
|---|---:|
| Top-1 candidate accuracy | 0.9775 |
| Top-3 candidate recall | 0.9982 |

The typo-type classifier has test accuracy **1.0000** on a stratified 80/20 split. This is a conditional result: its evaluation supplies the known correct candidate. End-to-end type accuracy can be lower when candidate ranking selects the wrong word. The synthetic typo rules also make type labels almost directly separable by edit distance and length difference.

## Run

```bash
cd T9-typo-correction
pip install -r requirements.txt
python simple_typo_corrector.py
python advanced_typo_corrector.py
python typo_type_classifier.py
```

Candidate generation uses the vocabulary derived from the included dataset, so it cannot correct words outside that closed vocabulary.
