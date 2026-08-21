import pandas as pd

from src.data_quality import (
    calculate_completeness_score,
    calculate_uniqueness_score,
    calculate_validity_score,
    evaluate_data_quality,
)


def test_complete_data_has_full_completeness_score():
    df = pd.DataFrame(
        {
            "Name": ["John Doe"],
            "Company": ["Example Corp"],
            "LinkedIn URL": [
                "https://www.linkedin.com/in/johndoe"
            ],
        }
    )

    assert calculate_completeness_score(df) == 100.0


def test_missing_required_field_reduces_completeness():
    df = pd.DataFrame(
        {
            "Name": ["John Doe"],
            "Company": [None],
            "LinkedIn URL": [
                "https://www.linkedin.com/in/johndoe"
            ],
        }
    )

    assert calculate_completeness_score(df) == 66.67


def test_duplicate_linkedin_urls_reduce_uniqueness():
    df = pd.DataFrame(
        {
            "Name": ["John", "Jane"],
            "Company": ["A", "B"],
            "LinkedIn URL": [
                "https://www.linkedin.com/in/same",
                "https://www.linkedin.com/in/same",
            ],
        }
    )

    assert calculate_uniqueness_score(df) == 50.0


def test_invalid_linkedin_url_reduces_validity():
    df = pd.DataFrame(
        {
            "Name": ["John", "Jane"],
            "Company": ["A", "B"],
            "LinkedIn URL": [
                "https://www.linkedin.com/in/john",
                "https://example.com/jane",
            ],
        }
    )

    assert calculate_validity_score(df) == 50.0


def test_good_data_passes_quality_threshold():
    df = pd.DataFrame(
        {
            "Name": ["John Doe"],
            "Company": ["Example Corp"],
            "LinkedIn URL": [
                "https://www.linkedin.com/in/johndoe"
            ],
            "Added On": ["2026-08-20"],
        }
    )

    result = evaluate_data_quality(df)

    assert result["overall_score"] >= 90
    assert result["status"] == "PASS"