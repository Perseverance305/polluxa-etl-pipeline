from pathlib import Path

from src.extraction import extract_leads


DATA_FILE = Path("data/raw/leads.csv")


def test_extract_leads_returns_dataframe():
    df = extract_leads(DATA_FILE)

    assert df is not None
    assert len(df) == 10


def test_extract_leads_contains_required_columns():
    df = extract_leads(DATA_FILE)

    required_columns = [
        "Name",
        "Company",
        "LinkedIn URL",
    ]

    for column in required_columns:
        assert column in df.columns