from datetime import datetime
from uuid import uuid4

from sqlalchemy import text

from src.database import engine


def start_pipeline_run(pipeline_name: str) -> str:
    """
    Create a new pipeline run record.

    Returns
    -------
    str
        UUID identifying the pipeline run.
    """

    run_id = str(uuid4())

    insert_sql = text(
        """
        INSERT INTO pipeline_runs (
            run_id,
            pipeline_name,
            started_at,
            status
        )
        VALUES (
            :run_id,
            :pipeline_name,
            :started_at,
            :status
        )
        """
    )

    with engine.begin() as connection:
        connection.execute(
            insert_sql,
            {
                "run_id": run_id,
                "pipeline_name": pipeline_name,
                "started_at": datetime.utcnow(),
                "status": "RUNNING",
            },
        )

    return run_id


def complete_pipeline_run(
    run_id: str,
    rows_extracted: int,
    rows_valid: int,
    rows_failed: int,
    rows_loaded: int,
):
    """
    Mark a pipeline run as successfully completed.
    """

    update_sql = text(
        """
        UPDATE pipeline_runs
        SET
            completed_at = :completed_at,
            rows_extracted = :rows_extracted,
            rows_valid = :rows_valid,
            rows_failed = :rows_failed,
            rows_loaded = :rows_loaded,
            status = 'SUCCESS'
        WHERE run_id = :run_id
        """
    )

    with engine.begin() as connection:
        connection.execute(
            update_sql,
            {
                "run_id": run_id,
                "completed_at": datetime.utcnow(),
                "rows_extracted": rows_extracted,
                "rows_valid": rows_valid,
                "rows_failed": rows_failed,
                "rows_loaded": rows_loaded,
            },
        )


def fail_pipeline_run(
    run_id: str,
    error_message: str,
    rows_extracted: int = 0,
    rows_valid: int = 0,
    rows_failed: int = 0,
    rows_loaded: int = 0,
):
    """
    Mark a pipeline run as failed and persist the error.
    """

    update_sql = text(
        """
        UPDATE pipeline_runs
        SET
            completed_at = :completed_at,
            rows_extracted = :rows_extracted,
            rows_valid = :rows_valid,
            rows_failed = :rows_failed,
            rows_loaded = :rows_loaded,
            status = 'FAILED',
            error_message = :error_message
        WHERE run_id = :run_id
        """
    )

    with engine.begin() as connection:
        connection.execute(
            update_sql,
            {
                "run_id": run_id,
                "completed_at": datetime.utcnow(),
                "rows_extracted": rows_extracted,
                "rows_valid": rows_valid,
                "rows_failed": rows_failed,
                "rows_loaded": rows_loaded,
                "error_message": error_message,
            },
        )