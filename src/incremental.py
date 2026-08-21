import pandas as pd


def filter_incremental_records(
    df: pd.DataFrame,
    watermark,
) -> pd.DataFrame:
    """
    Return records that are newer than the current watermark.

    If no watermark exists, all records are considered new.

    Records with the exact same timestamp as the watermark are
    retained so that timestamp ties cannot silently lose records.
    Database-level LinkedIn URL uniqueness provides idempotency.
    """

    if df.empty:
        return df.copy()

    if watermark is None:
        return df.copy()

    filtered = df.copy()

    added_dates = pd.to_datetime(
        filtered["Added On"],
        errors="coerce",
    )

    # Keep records at or after the watermark.
    #
    # Using >= rather than > protects against multiple records
    # sharing the same timestamp.
    mask = added_dates >= pd.Timestamp(watermark)

    return filtered.loc[mask].copy()