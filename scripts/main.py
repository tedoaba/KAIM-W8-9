import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
sys.path.append(os.path.abspath('../src'))

from data_loader import load_data

def main():
    file_path = '../data/data.csv'
    df = load_data(file_path=file_path)
    print(df.head())
    print(df.shape)
    print(df.isnull().sum())


if __name__ == '__main__':
    main()