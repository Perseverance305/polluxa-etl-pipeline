import pandas as pd


COLUMN_MAPPING = {
    "Name": "name",
    "Job Title": "job_title",
    "Company": "company",
    "Industry": "industry",
    "Location": "location",
    "Agent": "agent",
    "SDR Status": "sdr_status",
    "Comment Status": "comment_status",
    "Hot Score": "hot_score",
    "Source": "source",
    "Prioritized": "prioritized",
    "LinkedIn URL": "linkedin_url",
    "Added On": "added_at",
    "Last Contacted": "last_contacted_at",
    "Invite Sent At": "invite_sent_at",
    "Connected At": "connected_at",
}


DATE_COLUMNS = [
    "added_at",
    "last_contacted_at",
    "invite_sent_at",
    "connected_at",
]


TEXT_COLUMNS = [
    "name",
    "job_title",
    "company",
    "industry",
    "location",
    "agent",
    "sdr_status",
    "comment_status",
    "source",
]


def transform_leads(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform validated lead data into warehouse-ready format.

    The function is tolerant of optional columns so that it can
    transform both complete production datasets and smaller
    DataFrames used in unit tests.
    """

    transformed = df.copy()

    # ---------------------------------------------------------
    # 1. Rename source columns
    # ---------------------------------------------------------

    transformed = transformed.rename(columns=COLUMN_MAPPING)

    # ---------------------------------------------------------
    # 2. Normalize text fields
    # ---------------------------------------------------------

    for column in TEXT_COLUMNS:
        if column in transformed.columns:
            transformed[column] = (
                transformed[column]
                .fillna("")
                .astype(str)
                .str.strip()
            )

    # ---------------------------------------------------------
    # 3. Convert date columns
    # ---------------------------------------------------------

    for column in DATE_COLUMNS:
        if column in transformed.columns:
            transformed[column] = pd.to_datetime(
                transformed[column],
                errors="coerce"
            )

    # ---------------------------------------------------------
    # 4. Convert Hot Score to numeric
    # ---------------------------------------------------------

    if "hot_score" in transformed.columns:
        transformed["hot_score"] = pd.to_numeric(
            transformed["hot_score"],
            errors="coerce"
        )

    # ---------------------------------------------------------
    # 5. Convert Prioritized to boolean
    # ---------------------------------------------------------

    if "prioritized" in transformed.columns:
        transformed["prioritized"] = (
            transformed["prioritized"]
            .fillna("")
            .astype(str)
            .str.strip()
            .str.lower()
            .map({
                "yes": True,
                "no": False,
            })
            .astype(object)
        )
        
    return transformed