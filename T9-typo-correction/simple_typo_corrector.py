from difflib import get_close_matches
from pathlib import Path

import pandas as pd


DATA_PATH = Path(__file__).parent / "data" / "t9_typo_correction_dataset.csv"


def suggest_correction(word, candidates, n=5, cutoff=0.7):
    return get_close_matches(word, candidates, n=n, cutoff=cutoff)


def correct_sentence(sentence, candidates):
    corrected_words = []
    for word in sentence.split():
        suggestions = suggest_correction(word, candidates)
        corrected_words.append(suggestions[0] if suggestions else word)
    return " ".join(corrected_words)


def main():
    data = pd.read_csv(DATA_PATH)
    candidates = data["correct_word"].unique().tolist()
    sentence = "I am lerning pythom with hella fun"
    print("Original:", sentence)
    print("Corrected:", correct_sentence(sentence, candidates))


if __name__ == "__main__":
    main()
