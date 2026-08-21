import pandas as pd
from sqlalchemy import text

from src.database import engine


def load_leads(df: pd.DataFrame) -> int:
    """
    Load transformed lead records into PostgreSQL.

    Existing leads are identified by their LinkedIn URL and
    are not inserted again.

    Missing Pandas values are converted to Python None so
    PostgreSQL stores them as NULL.

    Returns
    -------
    int
        Number of records successfully inserted.
    """

    if df.empty:
        return 0

    records = df.to_dict(orient="records")

    # Convert Pandas missing values (NaN / NaT) to Python None.
    # PostgreSQL will store None as NULL.
    for record in records:
        for key, value in record.items():
            if pd.isna(value):
                record[key] = None

    insert_sql = text(
        """
        INSERT INTO leads (
            name,
            job_title,
            company,
            industry,
            location,
            agent,
            sdr_status,
            comment_status,
            hot_score,
            source,
            prioritized,
            linkedin_url,
            added_at,
            last_contacted_at,
            invite_sent_at,
            connected_at
        )
        VALUES (
            :name,
            :job_title,
            :company,
            :industry,
            :location,
            :agent,
            :sdr_status,
            :comment_status,
            :hot_score,
            :source,
            :prioritized,
            :linkedin_url,
            :added_at,
            :last_contacted_at,
            :invite_sent_at,
            :connected_at
        )
        ON CONFLICT (linkedin_url) DO NOTHING
        """
    )

    inserted = 0

    with engine.begin() as connection:

        for record in records:

            result = connection.execute(
                insert_sql,
                record
            )

            inserted += result.rowcount

    return inserted