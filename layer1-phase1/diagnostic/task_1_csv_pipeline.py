"""
Task 1: CSV Data Pipeline

Requirements:
1. Load the CSV file from data/sample_data.csv
2. Clean missing values (drop rows with NaN OR fill with appropriate values)
3. Compute groupby statistics (group by 'category', calculate sum and mean of 'value')
4. Output results to results.json

Expected output format:
{
    "total_rows": 100,
    "cleaned_rows": 95,
    "by_category": {
        "A": {"sum": 1234, "mean": 56.7},
        "B": {"sum": 2345, "mean": 67.8}
    }
}

Time: 20 minutes
"""

import pandas as pd
import json
from pathlib import Path


def load_and_clean_csv(file_path: str) -> pd.DataFrame:
    """Load CSV and clean missing values."""
    df = pd.read_csv(file_path)
    
    # TODO: Clean missing values (drop or fill)
    # Hint: df.dropna() or df.fillna()
    
    return df


def compute_groupby_stats(df: pd.DataFrame) -> dict:
    """Compute groupby statistics."""
    # TODO: Group by 'category' column
    # TODO: Calculate sum and mean of 'value' column
    # TODO: Return as dictionary
    pass


def main():
    """Main pipeline function."""
    # Get path to data file
    data_path = Path(__file__).parent / "data" / "sample_data.csv"
    
    # TODO: Load and clean data
    # TODO: Compute statistics
    # TODO: Save to results.json
    # TODO: Print summary
    pass


if __name__ == "__main__":
    main()
