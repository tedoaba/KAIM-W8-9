import pandas as pd

def load_data(file_path):
    """Load the dataset from a CSV file."""
    return pd.read_csv(file_path)

def handle_missing_values(df, method='mean', columns=None):
    if method == 'drop':
        df.dropna(inplace=True)
    elif method == 'mean':
        df[columns] = df[columns].fillna(df[columns].mean())
    elif method == 'median':
        df[columns] = df[columns].fillna(df[columns].median())
    return df
