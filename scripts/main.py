import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.append(os.path.abspath('../src'))

from data_cleaning import remove_duplicates, convert_data_types
from eda import univariate_analysis, bivariate_analysis
from feature_engineering import transaction_frequency, add_time_features
from scaling_encoding import normalize_features, encode_categorical_features
from utils import merge_ip_country
from data_loader import load_data, handle_missing_values, load_datasets, prepare_data
from model_definition import define_models
from train_evaluate import evaluate_models

def main():
    # Load data
    fraud_data_original = load_data('../data/Fraud_Data.csv')
    ip_data_original = load_data('../data/IpAddress_to_Country.csv')
    credit_data_original = load_data('../data/creditcard.csv')
    
    print(fraud_data_original.columns)
    print(ip_data_original.columns)
    print(credit_data_original.columns)

    print(fraud_data_original.info())
    print(ip_data_original.info())
    print(credit_data_original.info())

    # Load and prepare datasets
    fraud_data, credit_data = load_datasets('../data/cleaned_data_1.csv', '../data/cleaned_data_2.csv')
    datasets = prepare_data(fraud_data, credit_data)

    # Define models
    models = define_models()

    # Train and evaluate models, then log to MLflow
    evaluate_models(models, datasets)

    
if __name__ == '__main__':
    main()
