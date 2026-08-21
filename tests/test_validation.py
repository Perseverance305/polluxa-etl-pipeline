import pandas as pd

from src.validation import validate_leads


def test_valid_leads_pass_validation():
    df = pd.DataFrame(
        {
            "Name": ["John Doe"],
            "Company": ["Example Corp"],
            "LinkedIn URL": [
                "https://www.linkedin.com/in/johndoe"
            ],
            "Added On": ["2026-08-20"],
            "Last Contacted": ["2026-08-20 10:00"],
            "Invite Sent At": [None],
            "Connected At": ["2026-08-20 10:00"],
        }
    )

    valid, failed = validate_leads(df)

    assert len(valid) == 1
    assert len(failed) == 0


def test_missing_name_fails_validation():
    df = pd.DataFrame(
        {
            "Name": [""],
            "Company": ["Example Corp"],
            "LinkedIn URL": [
                "https://www.linkedin.com/in/johndoe"
            ],
            "Added On": ["2026-08-20"],
            "Last Contacted": [None],
            "Invite Sent At": [None],
            "Connected At": [None],
        }
    )

    valid, failed = validate_leads(df)

    assert len(valid) == 0
    assert len(failed) == 1
    assert "Missing required field: Name" in failed.iloc[0]["validation_error"]


def test_invalid_linkedin_url_fails_validation():
    df = pd.DataFrame(
        {
            "Name": ["John Doe"],
            "Company": ["Example Corp"],
            "LinkedIn URL": ["https://example.com/johndoe"],
            "Added On": ["2026-08-20"],
            "Last Contacted": [None],
            "Invite Sent At": [None],
            "Connected At": [None],
        }
    )

    valid, failed = validate_leads(df)

    assert len(valid) == 0
    assert len(failed) == 1
    assert "Invalid LinkedIn URL" in failed.iloc[0]["validation_error"]