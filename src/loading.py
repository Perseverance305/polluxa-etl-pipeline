import pandas as pd

from src.database import engine


def load_leads(df: pd.DataFrame) -> int:
    """
    Load transformed lead records into PostgreSQL.

    Returns the number of records loaded.
    """

    df.to_sql(
        "leads",
        con=engine,
        if_exists="append",
        index=False,
    )

    return len(df)
    