import pandas as pd


REQUIRED_COLUMNS = [
    "Name",
    "Company",
    "LinkedIn URL",
]

DATE_COLUMNS = [
    "Added On",
    "Last Contacted",
    "Invite Sent At",
    "Connected At",
]


def validate_leads(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Validate extracted lead records.

    Returns
    -------
    valid_df : pd.DataFrame
        Records that pass validation.

    failed_df : pd.DataFrame
        Records that fail validation.
    """

    df = df.copy()

    errors = pd.Series("", index=df.index, dtype="object")

    # ---------------------------------------------------------
    # 1. Required field validation
    # ---------------------------------------------------------

    for column in REQUIRED_COLUMNS:
        missing = df[column].isna() | (df[column].astype(str).str.strip() == "")

        errors.loc[missing] = (
            errors.loc[missing]
            + f"Missing required field: {column}; "
        )

    # ---------------------------------------------------------
    # 2. LinkedIn URL validation
    # ---------------------------------------------------------

    linkedin_url = df["LinkedIn URL"].fillna("").astype(str)

    invalid_url = (
        (linkedin_url != "")
        & ~linkedin_url.str.startswith("https://www.linkedin.com/")
    )

    errors.loc[invalid_url] = (
        errors.loc[invalid_url]
        + "Invalid LinkedIn URL; "
    )

    # ---------------------------------------------------------
    # 3. Date validation
    # ---------------------------------------------------------

    for column in DATE_COLUMNS:

        parsed_dates = pd.to_datetime(
            df[column],
            errors="coerce"
        )

        invalid_date = (
            df[column].notna()
            & (df[column].astype(str).str.strip() != "")
            & parsed_dates.isna()
        )

        errors.loc[invalid_date] = (
            errors.loc[invalid_date]
            + f"Invalid date in {column}; "
        )

    # ---------------------------------------------------------
    # 4. Duplicate detection
    # ---------------------------------------------------------

    duplicates = df.duplicated(
        subset=["LinkedIn URL"],
        keep="first"
    )

    errors.loc[duplicates] = (
        errors.loc[duplicates]
        + "Duplicate LinkedIn URL; "
    )

    # ---------------------------------------------------------
    # Separate valid and failed records
    # ---------------------------------------------------------

    failed_mask = errors != ""

    valid_df = df.loc[~failed_mask].copy()

    failed_df = df.loc[failed_mask].copy()

    failed_df["validation_error"] = errors.loc[failed_mask]

    return valid_df, failed_df
