"""
load_data.py
------------
Loads and validates the South Africa economic indicators dataset.
"""

import pandas as pd
import os
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def load_economic_data(filepath: str) -> pd.DataFrame:
    """
    Load and validate the SA economic indicators CSV.

    Args:
        filepath: Path to the CSV file.

    Returns:
        Cleaned DataFrame indexed by year.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Data file not found: {filepath}")

    df = pd.read_csv(filepath)
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df = df.dropna(subset=["year"])
    df = df.sort_values("year").reset_index(drop=True)

    logger.info(f"Loaded {len(df)} rows covering {int(df['year'].min())}–{int(df['year'].max())}.")
    return df


def get_summary(df: pd.DataFrame) -> None:
    """Print a quick dataset summary to console."""
    print("\n── Dataset Summary ───────────────────────────────────────")
    print(f"  Years covered  : {int(df['year'].min())} – {int(df['year'].max())}")
    print(f"  Indicators     : {len(df.columns) - 1}")
    print(f"  Missing values : {df.isnull().sum().sum()}")
    print(f"  Rows           : {len(df)}")
    print("─" * 58)


if __name__ == "__main__":
    df = load_economic_data("data/sa_economic_data.csv")
    get_summary(df)
    print(df.head())
  
