import sys
from pathlib import Path

import pandas as pd


PROJECT_DIR = Path(__file__).parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from advanced_typo_corrector import DATA_PATH, suggest_correction


def test_known_typo_includes_correct_candidate():
    data = pd.read_csv(DATA_PATH)
    candidates = data["correct_word"].unique().tolist()
    suggestions = suggest_correction("pythom", candidates)
    assert "python" in [word for word, _ in suggestions]
