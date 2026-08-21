from sqlalchemy import text

from src.database import engine


def save_dq_result(
    run_id: str,
    pipeline_name: str,
    dq_result: dict,
) -> None:
    """
    Persist the Data Quality result for a pipeline run.
    """

    insert_sql = text(
        """
        INSERT INTO dq_results (
            run_id,
            pipeline_name,
            completeness_score,
            uniqueness_score,
            validity_score,
            timeliness_score,
            referential_integrity_score,
            overall_score,
            status
        )
        VALUES (
            :run_id,
            :pipeline_name,
            :completeness_score,
            :uniqueness_score,
            :validity_score,
            :timeliness_score,
            :referential_integrity_score,
            :overall_score,
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
                "completeness_score": float(
                    dq_result["completeness_score"]
                ),
                "uniqueness_score": float(
                    dq_result["uniqueness_score"]
                ),
                "validity_score": float(
                    dq_result["validity_score"]
                ),
                "timeliness_score": float(
                    dq_result["timeliness_score"]
                ),
                "referential_integrity_score": float(
                    dq_result["referential_integrity_score"]
                ),
                "overall_score": float(
                    dq_result["overall_score"]
                ),
                "status": dq_result["status"],
            },
        )
