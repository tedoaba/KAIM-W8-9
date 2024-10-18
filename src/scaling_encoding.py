from sklearn.preprocessing import StandardScaler, LabelEncoder

def normalize_features(df, columns):
    """Normalize the numerical features using StandardScaler."""
    scaler = StandardScaler()
    df[columns] = scaler.fit_transform(df[columns])
    return df

def encode_categorical_features(df, columns):
    """Encode categorical features using LabelEncoder."""
    le = LabelEncoder()
    for column in columns:
        df[column] = le.fit_transform(df[column])
    return df
