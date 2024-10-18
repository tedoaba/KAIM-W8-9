import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.append(os.path.abspath('../src'))

from data_preprocessing import load_data, handle_missing_values
from data_cleaning import remove_duplicates, convert_data_types
from eda import univariate_analysis, bivariate_analysis
from feature_engineering import transaction_frequency, add_time_features
from scaling_encoding import normalize_features, encode_categorical_features
from utils import merge_ip_country

def main():
    # Load data
    fraud_data = load_data('../data/Fraud_Data.csv')
    ip_data = load_data('../data/IpAddress_to_Country.csv')
    
    # Handle missing values
    fraud_data = handle_missing_values(fraud_data, method='mean', columns=['age'])
    
    # Data cleaning
    fraud_data = remove_duplicates(fraud_data)
    fraud_data = convert_data_types(fraud_data, ['signup_time', 'purchase_time'], 'datetime')
    
    # Exploratory Data Analysis
    univariate_analysis(fraud_data, 'purchase_value')
    bivariate_analysis(fraud_data, 'purchase_value', 'class')
    
    # Merge with geolocation data
    fraud_data = merge_ip_country(fraud_data, ip_data)
    
    # Feature Engineering
    #fraud_data = transaction_frequency(fraud_data, 'user_id')
    #fraud_data = add_time_features(fraud_data, 'purchase_time')
    # Debugging: Print columns of the DataFrame
    print(fraud_data.columns)

    # Check if 'purchase_time' exists
    if 'purchase_time' in fraud_data.columns:
        # Proceed with adding time features
        fraud_data = add_time_features(fraud_data, 'purchase_time')
    else:
        raise KeyError("'purchase_time' column not found in the dataset")

    #fraud_data = transaction_frequency(fraud_data, 'user_id')
    #print(fraud_data.head())
    # Scaling and Encoding
    fraud_data = normalize_features(fraud_data, ['purchase_value', 'age'])
    fraud_data = encode_categorical_features(fraud_data, ['source', 'browser', 'sex'])

if __name__ == '__main__':
    main()
