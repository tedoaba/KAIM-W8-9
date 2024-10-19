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
    credit_data = load_data('../data/creditcard.csv')
    
    print(fraud_data.columns)
    print(ip_data.columns)
    print(credit_data.columns)

    print(fraud_data.info())
    print(ip_data.info())
    print(credit_data.info())

if __name__ == '__main__':
    main()
