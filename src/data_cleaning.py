import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def remove_duplicates(df):
    """Remove duplicate entries from the dataset."""
    return df.drop_duplicates()

def convert_data_types(df, columns, target_type):
    """
    Convert specified columns to the target data type.
    
    Args:
    - df: DataFrame
    - columns: List of columns to convert
    - target_type: Target data type (e.g., 'datetime', 'category')
    
    Returns:
    - df: DataFrame with converted column types.
    """
    if target_type == 'datetime':
        for column in columns:
            try:
                # Convert columns to datetime, automatically infer the format
                df[column] = pd.to_datetime(df[column], errors='coerce')
                # Handle any missing/invalid datetime by filling with a placeholder value
                df[column] = df[column].fillna(pd.Timestamp('1900-01-01'))
            except Exception as e:
                print(f"Error converting {column} to datetime: {e}")
    elif target_type == 'category':
        df[columns] = df[columns].astype('category')
    return df
