from pathlib import Path

from src.extraction import extract_leads
from src.validation import validate_leads
from src.transformation import transform_leads
from src.loading import load_leads
from src.pipeline_metadata import (
    start_pipeline_run,
    complete_pipeline_run,
    fail_pipeline_run,
)


PIPELINE_NAME = "linkedin_leads_pipeline"


def save_failed_records(df):
    """Save validation failures for review and remediation."""

    if df.empty:
        return

    failed_dir = Path("data/failed")
    failed_dir.mkdir(parents=True, exist_ok=True)

    failed_file = failed_dir / "failed_leads.csv"
    df.to_csv(failed_file, index=False)

    print(f"Failed records saved to: {failed_file}")


def main():
    file_path = Path("data/raw/leads.csv")

    run_id = start_pipeline_run(PIPELINE_NAME)

    rows_extracted = 0
    rows_valid = 0
    rows_failed = 0
    rows_loaded = 0

    try:
        # ---------------------------------------------------------
        # Extract
        # ---------------------------------------------------------

        df = extract_leads(file_path)

        rows_extracted = len(df)

        # ---------------------------------------------------------
        # Validate
        # ---------------------------------------------------------

        valid_df, failed_df = validate_leads(df)

        rows_valid = len(valid_df)
        rows_failed = len(failed_df)

        print(f"Valid records: {rows_valid}")
        print(f"Failed records: {rows_failed}")

        # ---------------------------------------------------------
        # Save validation failures
        # ---------------------------------------------------------

        save_failed_records(failed_df)

        # ---------------------------------------------------------
        # Transform
        # ---------------------------------------------------------

        transformed_df = transform_leads(valid_df)

        # ---------------------------------------------------------
        # Load
        # ---------------------------------------------------------

        rows_loaded = load_leads(transformed_df)

        print(f"Records loaded: {rows_loaded}")

        # ---------------------------------------------------------
        # Mark successful run
        # ---------------------------------------------------------

        complete_pipeline_run(
            run_id=run_id,
            rows_extracted=rows_extracted,
            rows_valid=rows_valid,
            rows_failed=rows_failed,
            rows_loaded=rows_loaded,
        )

        print(f"Pipeline run completed successfully: {run_id}")

    except Exception as exc:

        fail_pipeline_run(
            run_id=run_id,
            error_message=str(exc),
            rows_extracted=rows_extracted,
            rows_valid=rows_valid,
            rows_failed=rows_failed,
            rows_loaded=rows_loaded,
        )

        print(f"Pipeline run failed: {run_id}")
        print(f"Error: {exc}")

        raise


if __name__ == "__main__":
    main()