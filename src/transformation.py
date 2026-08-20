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


def transform_leads(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform validated lead data into warehouse-ready format.
    """

    transformed = df.copy()

    # Rename source columns to database-friendly names
    transformed = transformed.rename(columns=COLUMN_MAPPING)

    # Convert date columns to proper datetime values
    for column in DATE_COLUMNS:
        transformed[column] = pd.to_datetime(
            transformed[column],
            errors="coerce"
        )

    # Normalize text fields
    text_columns = [
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

    for column in text_columns:
        transformed[column] = (
            transformed[column]
            .fillna("")
            .astype(str)
            .str.strip()
        )

    # Convert Hot Score to numeric
    transformed["hot_score"] = pd.to_numeric(
        transformed["hot_score"],
        errors="coerce"
    )

    # Convert Prioritized to boolean
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
    )

    return transformed