import pandas as pd


DQ_PASS_THRESHOLD = 90.0


def calculate_completeness_score(df: pd.DataFrame) -> float:
    """
    Measure the percentage of required fields that are populated.
    """

    required_columns = [
        "Name",
        "Company",
        "LinkedIn URL",
    ]

    if df.empty:
        return 100.0

    total_fields = len(df) * len(required_columns)

    populated_fields = sum(
        df[column]
        .notna()
        .astype(bool)
        .sum()
        for column in required_columns
        if column in df.columns
    )

    if total_fields == 0:
        return 0.0

    return round(
        (populated_fields / total_fields) * 100,
        2,
    )


def calculate_uniqueness_score(df: pd.DataFrame) -> float:
    """
    Measure uniqueness of LinkedIn URLs.
    """

    if df.empty:
        return 100.0

    if "LinkedIn URL" not in df.columns:
        return 0.0

    non_null_urls = df["LinkedIn URL"].dropna()

    if non_null_urls.empty:
        return 0.0

    unique_urls = non_null_urls.nunique()

    return round(
        (unique_urls / len(non_null_urls)) * 100,
        2,
    )


def calculate_validity_score(df: pd.DataFrame) -> float:
    """
    Measure validity of LinkedIn URLs.
    """

    if df.empty:
        return 100.0

    if "LinkedIn URL" not in df.columns:
        return 0.0

    non_null_urls = df["LinkedIn URL"].dropna()

    if non_null_urls.empty:
        return 0.0

    valid_urls = non_null_urls.astype(str).str.startswith(
        "https://www.linkedin.com/"
    )

    return round(
        valid_urls.mean() * 100,
        2,
    )


def calculate_timeliness_score(
    df: pd.DataFrame,
    maximum_age_days: int = 7,
) -> float:
    """
    Measure whether records are recent enough for operational use.

    Records older than maximum_age_days receive a failing
    timeliness score.
    """

    if df.empty:
        return 100.0

    if "Added On" not in df.columns:
        return 0.0

    dates = pd.to_datetime(
        df["Added On"],
        errors="coerce",
    )

    valid_dates = dates.dropna()

    if valid_dates.empty:
        return 0.0

    reference_date = valid_dates.max()

    age_days = (
        reference_date - valid_dates
    ).dt.days

    timely = age_days <= maximum_age_days

    return round(
        timely.mean() * 100,
        2,
    )


def calculate_referential_integrity_score(
    df: pd.DataFrame,
) -> float:
    """
    Measure whether key relationship fields are present.

    For the current lead model, Name, Company and LinkedIn URL
    form the minimum business relationship required for a
    lead to be represented correctly.
    """

    required_columns = [
        "Name",
        "Company",
        "LinkedIn URL",
    ]

    if df.empty:
        return 100.0

    if not all(
        column in df.columns
        for column in required_columns
    ):
        return 0.0

    valid_records = df[required_columns].notna().all(axis=1)

    return round(
        valid_records.mean() * 100,
        2,
    )


def calculate_overall_score(
    completeness: float,
    uniqueness: float,
    validity: float,
    timeliness: float,
    referential_integrity: float,
) -> float:
    """
    Calculate the weighted composite Data Quality score.

    Weights:
        Completeness: 25%
        Uniqueness: 20%
        Validity: 25%
        Timeliness: 15%
        Referential Integrity: 15%
    """

    score = (
        completeness * 0.25
        + uniqueness * 0.20
        + validity * 0.25
        + timeliness * 0.15
        + referential_integrity * 0.15
    )

    return round(score, 2)


def evaluate_data_quality(
    df: pd.DataFrame,
) -> dict:
    """
    Run all Data Quality checks and return the complete result.
    """

    completeness = calculate_completeness_score(df)
    uniqueness = calculate_uniqueness_score(df)
    validity = calculate_validity_score(df)
    timeliness = calculate_timeliness_score(df)
    referential_integrity = (
        calculate_referential_integrity_score(df)
    )

    overall_score = calculate_overall_score(
        completeness,
        uniqueness,
        validity,
        timeliness,
        referential_integrity,
    )

    status = (
        "PASS"
        if overall_score >= DQ_PASS_THRESHOLD
        else "FAIL"
    )

    return {
        "completeness_score": completeness,
        "uniqueness_score": uniqueness,
        "validity_score": validity,
        "timeliness_score": timeliness,
        "referential_integrity_score": referential_integrity,
        "overall_score": overall_score,
        "status": status,
    }