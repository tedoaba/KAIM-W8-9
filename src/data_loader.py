import pandas as pd
from sklearn.model_selection import train_test_split

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

def load_datasets(fraud_path, credit_path):
    """Load datasets from CSV files."""
    fraud_data = pd.read_csv(fraud_path)
    credit_data = pd.read_csv(credit_path)
    return fraud_data, credit_data


def prepare_data(fraud_data, credit_data):
    """Prepare train and test datasets."""
    X1 = fraud_data.drop(columns=['Class'])
    y1 = fraud_data['Class']
    
    X2 = credit_data.drop(columns=['Class'])
    y2 = credit_data['Class']

    # Train-test split
    X_train1, X_test1, y_train1, y_test1 = train_test_split(X1, y1, test_size=0.2, random_state=42)
    X_train2, X_test2, y_train2, y_test2 = train_test_split(X2, y2, test_size=0.2, random_state=42)
    
    # Datasets dictionary
    datasets = {
        "fraud_data": (X_train1, y_train1, X_test1, y_test1),
        "credit_data": (X_train2, y_train2, X_test2, y_test2),
    }
    return datasets
