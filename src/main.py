from pathlib import Path
import pandas as pd


def extract_leads(file_path: str) -> pd.DataFrame:
    """Read the Polluxa leads CSV into a pandas DataFrame."""

    print(f"Reading source file: {file_path}")

    df = pd.read_csv(file_path)

    print(f"Rows extracted: {len(df)}")
    print(f"Columns found: {list(df.columns)}")

    return df


def main():
    file_path = Path("data/raw/leads.csv")

    df = extract_leads(file_path)

    print("\nFirst 5 records:")
    print(df.head())


if __name__ == "__main__":
    main()