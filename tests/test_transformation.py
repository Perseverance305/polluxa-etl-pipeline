import pandas as pd

from src.transformation import transform_leads


def test_transform_leads_renames_columns():
    df = pd.DataFrame(
        {
            "Name": [" John Doe "],
            "Job Title": [" Data Analyst "],
            "Company": [" Example Corp "],
            "Industry": [" Technology "],
            "Location": [" Johannesburg "],
            "Agent": [" Percy Maphanga "],
            "SDR Status": [" connected "],
            "Comment Status": [" No post "],
            "Hot Score": ["85"],
            "Source": [" Build Search "],
            "Prioritized": ["Yes"],
            "LinkedIn URL": [
                "https://www.linkedin.com/in/johndoe"
            ],
            "Added On": ["2026-08-20"],
            "Last Contacted": ["2026-08-20 10:00"],
            "Invite Sent At": [None],
            "Connected At": ["2026-08-20 10:00"],
        }
    )

    transformed = transform_leads(df)

    assert "name" in transformed.columns
    assert "job_title" in transformed.columns
    assert "linkedin_url" in transformed.columns

    assert "Name" not in transformed.columns


def test_transform_leads_cleans_text():
    df = pd.DataFrame(
        {
            "Name": [" John Doe "],
            "Company": [" Example Corp "],
            "LinkedIn URL": [
                "https://www.linkedin.com/in/johndoe"
            ],
        }
    )

    transformed = transform_leads(df)

    assert transformed.iloc[0]["name"] == "John Doe"
    assert transformed.iloc[0]["company"] == "Example Corp"


def test_transform_leads_converts_hot_score():
    df = pd.DataFrame(
        {
            "Name": ["John Doe"],
            "Company": ["Example Corp"],
            "Hot Score": ["85"],
            "LinkedIn URL": [
                "https://www.linkedin.com/in/johndoe"
            ],
        }
    )

    transformed = transform_leads(df)

    assert transformed.iloc[0]["hot_score"] == 85.0


def test_transform_leads_converts_prioritized_to_boolean():
    df = pd.DataFrame(
        {
            "Name": ["John Doe", "Jane Doe"],
            "Company": ["Example Corp", "Example Inc"],
            "Prioritized": ["Yes", "No"],
            "LinkedIn URL": [
                "https://www.linkedin.com/in/johndoe",
                "https://www.linkedin.com/in/janedoe",
            ],
        }
    )

    transformed = transform_leads(df)

    assert transformed.iloc[0]["prioritized"] is True
    assert transformed.iloc[1]["prioritized"] is False