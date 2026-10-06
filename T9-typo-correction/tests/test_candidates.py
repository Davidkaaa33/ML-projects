import sys
from pathlib import Path

import pandas as pd

PROJECT_DIR = Path(__file__).parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from advanced_typo_corrector import (
    DATA_PATH,
    correct_sentence,
    suggest_correction,
)


def vocabulary():
    data = pd.read_csv(DATA_PATH)
    return data["correct_word"].dropna().unique().tolist()


def test_known_typo_includes_correct_candidate():
    suggestions = suggest_correction("pythom", vocabulary())
    assert "python" in [word for word, _ in suggestions]


def test_empty_input_returns_no_candidates():
    assert suggest_correction("", vocabulary()) == []
    assert suggest_correction("   ", vocabulary()) == []


def test_non_positive_top_n_returns_no_candidates():
    assert suggest_correction("pythom", vocabulary(), top_n=0) == []


def test_candidate_ranking_is_deterministic():
    first = suggest_correction("pythom", vocabulary(), top_n=3)
    second = suggest_correction("pythom", vocabulary(), top_n=3)

    assert first == second
    assert len(first) <= 3


def test_sentence_correction_preserves_known_words():
    candidates = ["i", "am", "learning", "python", "with", "fun"]
    corrected = correct_sentence("I am lerning pythom with fun", candidates)

    assert corrected == "I am learning python with fun"
