from pathlib import Path

import pandas as pd

from src.extraction import extract_leads
from src.validation import validate_leads
from src.transformation import transform_leads
from src.loading import load_leads

from src.pipeline_metadata import (
    start_pipeline_run,
    complete_pipeline_run,
    fail_pipeline_run,
)

from src.watermark import (
    get_watermark,
    set_watermark,
)

from src.incremental import (
    filter_incremental_records,
)

from src.data_quality import (
    evaluate_data_quality,
)

from src.dq_metadata import (
    save_dq_result,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

PIPELINE_NAME = "linkedin_leads_pipeline"


def save_failed_records(df):
    """Save validation failures for review and remediation."""

    if df.empty:
        return

    project_root = Path(__file__).resolve().parent.parent
    failed_dir = project_root / "data" / "failed"
    failed_dir.mkdir(parents=True, exist_ok=True)

    failed_file = failed_dir / "failed_leads.csv"
    df.to_csv(failed_file, index=False)

    print(f"Failed records saved to: {failed_file}")


def main():
    project_root = Path(__file__).resolve().parent.parent
    file_path = project_root / "data" / "raw" / "leads.csv"

    # ---------------------------------------------------------
    # Start pipeline run
    # ---------------------------------------------------------

    run_id = start_pipeline_run(PIPELINE_NAME)

    rows_extracted = 0
    rows_valid = 0
    rows_failed = 0
    rows_loaded = 0

    try:

        # -----------------------------------------------------
        # Extract
        # -----------------------------------------------------

        df = extract_leads(file_path)

        rows_extracted = len(df)

        print(f"Rows extracted: {rows_extracted}")

        # -----------------------------------------------------
        # Get current watermark
        # -----------------------------------------------------

        watermark = get_watermark(PIPELINE_NAME)

        print(f"Current watermark: {watermark}")

        # -----------------------------------------------------
        # Incremental filtering
        # -----------------------------------------------------

        incremental_df = filter_incremental_records(
            df,
            watermark,
        )

        print(
            f"Records after incremental filtering: "
            f"{len(incremental_df)}"
        )

        # -----------------------------------------------------
        # Validation
        # -----------------------------------------------------

        valid_df, failed_df = validate_leads(
            incremental_df
        )

        rows_valid = len(valid_df)
        rows_failed = len(failed_df)

        print(f"Valid records: {rows_valid}")
        print(f"Failed records: {rows_failed}")

        # -----------------------------------------------------
        # Save validation failures
        # -----------------------------------------------------

        save_failed_records(failed_df)

        # -----------------------------------------------------
        # Data Quality
        #
        # DQ is evaluated BEFORE loading data.
        # If the DQ threshold fails, the pipeline stops
        # before bad data reaches the warehouse.
        # -----------------------------------------------------

        dq_result = evaluate_data_quality(valid_df)

        print("Data Quality Results:")
        print(
            f"Completeness: "
            f"{dq_result['completeness_score']}%"
        )
        print(
            f"Uniqueness: "
            f"{dq_result['uniqueness_score']}%"
        )
        print(
            f"Validity: "
            f"{dq_result['validity_score']}%"
        )
        print(
            f"Timeliness: "
            f"{dq_result['timeliness_score']}%"
        )
        print(
            f"Referential Integrity: "
            f"{dq_result['referential_integrity_score']}%"
        )
        print(
            f"Overall DQ Score: "
            f"{dq_result['overall_score']}%"
        )
        print(
            f"DQ Status: "
            f"{dq_result['status']}"
        )

        # -----------------------------------------------------
        # Persist DQ result
        # -----------------------------------------------------

        save_dq_result(
            run_id=run_id,
            pipeline_name=PIPELINE_NAME,
            dq_result=dq_result,
        )

        # -----------------------------------------------------
        # DQ threshold gate
        # -----------------------------------------------------

        if dq_result["status"] == "FAIL":
            raise RuntimeError(
                "Data Quality threshold failed: "
                f"{dq_result['overall_score']}%"
            )

        # -----------------------------------------------------
        # Transform
        # -----------------------------------------------------

        transformed_df = transform_leads(valid_df)

        # -----------------------------------------------------
        # Load
        # -----------------------------------------------------

        rows_loaded = load_leads(transformed_df)

        print(f"Records loaded: {rows_loaded}")

        # -----------------------------------------------------
        # Advance watermark ONLY after successful load
        # -----------------------------------------------------

        if not incremental_df.empty:

            transformed_dates = pd.to_datetime(
                incremental_df["Added On"],
                errors="coerce",
            )

            latest_timestamp = transformed_dates.max()

            if pd.notna(latest_timestamp):

                set_watermark(
                    PIPELINE_NAME,
                    latest_timestamp.to_pydatetime(),
                )

                print(
                    f"Watermark updated to: "
                    f"{latest_timestamp}"
                )

        # -----------------------------------------------------
        # Mark successful run
        # -----------------------------------------------------

        complete_pipeline_run(
            run_id=run_id,
            rows_extracted=rows_extracted,
            rows_valid=rows_valid,
            rows_failed=rows_failed,
            rows_loaded=rows_loaded,
        )

        print(
            f"Pipeline run completed successfully: {run_id}"
        )

    except Exception as exc:

        # -----------------------------------------------------
        # Persist failed pipeline run
        # -----------------------------------------------------

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