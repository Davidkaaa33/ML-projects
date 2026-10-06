import pytest

from app.confidence import parse_threshold, select_threshold


def test_parse_threshold_accepts_cosine_range():
    assert parse_threshold("0.55") == 0.55
    assert parse_threshold("") is None
    assert parse_threshold(None) is None


def test_parse_threshold_rejects_invalid_range():
    with pytest.raises(ValueError):
        parse_threshold("1.2")


def test_select_threshold_separates_supported_from_unsupported():
    records = [
        {"answerable": True, "top_score": 0.82},
        {"answerable": True, "top_score": 0.71},
        {"answerable": False, "top_score": 0.31},
        {"answerable": False, "top_score": 0.20},
    ]

    selected = select_threshold(records)

    assert 0.31 < selected["threshold"] < 0.71
    assert selected["balanced_accuracy"] == 1.0
    assert selected["answerable_recall"] == 1.0
    assert selected["unanswerable_recall"] == 1.0
