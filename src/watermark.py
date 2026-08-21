from datetime import datetime

from sqlalchemy import text

from src.database import engine


def get_watermark(pipeline_name: str):
    """
    Return the current watermark for a pipeline.

    Returns None if no watermark has been recorded yet.
    """

    query = text(
        """
        SELECT watermark_value
        FROM pipeline_watermarks
        WHERE pipeline_name = :pipeline_name
        """
    )

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {"pipeline_name": pipeline_name},
        ).scalar()

    return result


def set_watermark(
    pipeline_name: str,
    watermark_value: datetime,
):
    """
    Create or update the watermark for a pipeline.
    """

    query = text(
        """
        INSERT INTO pipeline_watermarks (
            pipeline_name,
            watermark_value,
            updated_at
        )
        VALUES (
            :pipeline_name,
            :watermark_value,
            CURRENT_TIMESTAMP
        )
        ON CONFLICT (pipeline_name)
        DO UPDATE SET
            watermark_value = EXCLUDED.watermark_value,
            updated_at = CURRENT_TIMESTAMP
        """
    )

    with engine.begin() as connection:
        connection.execute(
            query,
            {
                "pipeline_name": pipeline_name,
                "watermark_value": watermark_value,
            },
        )