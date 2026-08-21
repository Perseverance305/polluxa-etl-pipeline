from pathlib import Path

import pandas as pd

from src.main import save_failed_records


def test_save_failed_records(tmp_path):
    failed_df = pd.DataFrame(
        {
            "Name": [None],
            "Company": ["Example Corp"],
            "LinkedIn URL": [
                "https://www.linkedin.com/in/example"
            ],
            "validation_error": [
                "Missing required field: Name;"
            ],
        }
    )

    original_cwd = Path.cwd()

    try:
        import os

        os.chdir(tmp_path)

        save_failed_records(failed_df)

        failed_file = (
            tmp_path
            / "data"
            / "failed"
            / "failed_leads.csv"
        )

        assert failed_file.exists()

        saved_df = pd.read_csv(failed_file)

        assert len(saved_df) == 1
        assert saved_df.iloc[0]["Company"] == "Example Corp"
        assert (
            saved_df.iloc[0]["validation_error"]
            == "Missing required field: Name;"
        )

    finally:
        os.chdir(original_cwd)