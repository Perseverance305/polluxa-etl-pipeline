import pandas as pd


def extract_leads(file_path: str) -> pd.DataFrame:
    """
    Extract lead data from a CSV file.

    Parameters
    ----------
    file_path : str
        Path to the source CSV file.

    Returns
    -------
    pd.DataFrame
        Raw lead data.
    """

    print(f"Reading source file: {file_path}")

    df = pd.read_csv(file_path)

    print(f"Rows extracted: {len(df)}")
    print(f"Columns found: {df.columns.tolist()}")

    return df