import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def transaction_frequency(df, user_column):
    """Calculate transaction frequency for each user."""
    return df.groupby(user_column).size().reset_index(name='transaction_count')

def add_time_features(df, time_column):
    """Create time-based features such as hour of day and day of week."""
    df['hour_of_day'] = pd.to_datetime(df[time_column]).dt.hour
    df['day_of_week'] = pd.to_datetime(df[time_column]).dt.dayofweek
    return df
