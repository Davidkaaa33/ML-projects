import json
from pathlib import Path

import Levenshtein
import pandas as pd


PROJECT_DIR = Path(__file__).parent
DATA_PATH = PROJECT_DIR / "data" / "t9_typo_correction_dataset.csv"
RESULTS_PATH = PROJECT_DIR / "artifacts" / "candidate_results.json"


def calculate_score(typo_word, candidate_word):
    score = 0
    if typo_word[0] == candidate_word[0]:
        score += 2
    if typo_word[-1] == candidate_word[-1]:
        score += 2
    score += max(0, 10 - Levenshtein.distance(typo_word, candidate_word))
    score += max(0, 2 - abs(len(typo_word) - len(candidate_word)))
    return score


def suggest_correction(typo_word, candidate_words, top_n=3):
    typo_word = typo_word.strip().lower()
    if not typo_word or top_n <= 0:
        return []

    normalized_candidates = [
        word.lower()
        for word in candidate_words
        if isinstance(word, str) and word
    ]
    candidates = [
        word
        for word in normalized_candidates
        if word[0] == typo_word[0] and Levenshtein.distance(typo_word, word) <= 2
    ]
    scored_candidates = [
        (word, calculate_score(typo_word, word)) for word in candidates
    ]
    return sorted(scored_candidates, key=lambda item: (-item[1], item[0]))[:top_n]


def correct_sentence(sentence, candidate_words):
    corrected_words = []
    for original_word in sentence.split():
        word = original_word.lower()
        if len(word) <= 2 or word in candidate_words:
            corrected_words.append(original_word)
            continue
        suggestions = suggest_correction(word, candidate_words)
        corrected_words.append(suggestions[0][0] if suggestions else original_word)
    return " ".join(corrected_words)


def evaluate_candidate_ranking(data, candidate_words):
    top_1_correct = 0
    top_3_correct = 0
    for row in data.itertuples():
        suggestions = suggest_correction(row.typo_word, candidate_words)
        words = [word for word, _ in suggestions]
        top_1_correct += bool(words and words[0] == row.correct_word)
        top_3_correct += row.correct_word in words
    count = len(data)
    return {"top_1_accuracy": top_1_correct / count, "top_3_recall": top_3_correct / count}


def main():
    data = pd.read_csv(DATA_PATH)
    candidate_words = data["correct_word"].unique().tolist()
    metrics = evaluate_candidate_ranking(data, candidate_words)
    print("Candidate ranking metrics:")
    for metric, value in metrics.items():
        print(f"{metric}: {value:.4f}")

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "generated_by": "advanced_typo_corrector.py",
                "dataset": {
                    "path": "data/t9_typo_correction_dataset.csv",
                    "synthetic": True,
                    "rows": int(len(data)),
                },
                "candidate_source": "closed vocabulary from dataset",
                "metrics": {key: float(value) for key, value in metrics.items()},
            },
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )
    print(f"Saved metrics to {RESULTS_PATH}")

    sentence = "I am lerning pythom with hella fun"
    print("Original:", sentence)
    print("Corrected:", correct_sentence(sentence, candidate_words))


if __name__ == "__main__":
    main()
