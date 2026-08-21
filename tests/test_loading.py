import pandas as pd
from sqlalchemy import text

from src.database import engine
from src.loading import load_leads


def test_load_leads_is_idempotent():
    test_url = "https://www.linkedin.com/in/test-idempotency"

    test_df = pd.DataFrame(
        {
            "name": ["Idempotency Test"],
            "job_title": ["Data Analyst"],
            "company": ["Test Company"],
            "industry": ["Technology"],
            "location": ["Johannesburg"],
            "agent": ["Test Agent"],
            "sdr_status": ["connected"],
            "comment_status": ["No post"],
            "hot_score": [85.0],
            "source": ["Test"],
            "prioritized": [True],
            "linkedin_url": [test_url],
            "added_at": [pd.Timestamp("2026-08-20")],
            "last_contacted_at": [None],
            "invite_sent_at": [None],
            "connected_at": [pd.Timestamp("2026-08-20 10:00")],
        }
    )

    try:
        # First load should insert the record.
        first_inserted = load_leads(test_df)

        # Second load should be ignored because the LinkedIn URL
        # already exists.
        second_inserted = load_leads(test_df)

        assert first_inserted == 1
        assert second_inserted == 0

        with engine.connect() as connection:
            result = connection.execute(
                text(
                    """
                    SELECT COUNT(*)
                    FROM leads
                    WHERE linkedin_url = :linkedin_url
                    """
                ),
                {"linkedin_url": test_url},
            )

            count = result.scalar()

        assert count == 1

    finally:
        # Clean up the test record.
        with engine.begin() as connection:
            connection.execute(
                text(
                    """
                    DELETE FROM leads
                    WHERE linkedin_url = :linkedin_url
                    """
                ),
                {"linkedin_url": test_url},
            )