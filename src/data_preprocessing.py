import pandas as pd

def load_data(file_path):
    """Load the dataset from a CSV file."""
    return pd.read_csv(file_path)

def handle_missing_values(df, method='mean', columns=None):
    """
    Handle missing values by either dropping or imputing.
    Args:
    - df: DataFrame with missing values.
    - method: Strategy to handle missing values ('mean', 'median', or 'drop').
    - columns: List of columns to impute; None applies to all columns.
    """
    if method == 'drop':
        df.dropna(inplace=True)
    elif method == 'mean':
        df[columns] = df[columns].fillna(df[columns].mean())
    elif method == 'median':
        df[columns] = df[columns].fillna(df[columns].median())
    return df
