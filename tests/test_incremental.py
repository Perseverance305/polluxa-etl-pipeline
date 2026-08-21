import pandas as pd

from src.incremental import filter_incremental_records


def test_no_watermark_returns_all_records():

    df = pd.DataFrame(
        {
            "Name": ["A", "B"],
            "Added On": [
                "2026-08-20",
                "2026-08-21",
            ],
        }
    )

    result = filter_incremental_records(
        df,
        None,
    )

    assert len(result) == 2


def test_watermark_keeps_newer_records():

    df = pd.DataFrame(
        {
            "Name": ["A", "B", "C"],
            "Added On": [
                "2026-08-19",
                "2026-08-20",
                "2026-08-21",
            ],
        }
    )

    watermark = pd.Timestamp("2026-08-20")

    result = filter_incremental_records(
        df,
        watermark,
    )

    assert len(result) == 2
    assert list(result["Name"]) == ["B", "C"]


def test_watermark_keeps_timestamp_ties():

    df = pd.DataFrame(
        {
            "Name": ["A", "B"],
            "Added On": [
                "2026-08-20",
                "2026-08-20",
            ],
        }
    )

    watermark = pd.Timestamp("2026-08-20")

    result = filter_incremental_records(
        df,
        watermark,
    )

    assert len(result) == 2