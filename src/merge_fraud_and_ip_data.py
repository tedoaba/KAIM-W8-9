import pandas as pd

fraud_data = pd.read_csv('../data/Fraud_Data.csv')
ip_data = pd.read_csv('../data/IpAddress_to_Country.csv')

merged_df = pd.concat([fraud_data, ip_data], axis = 1)
merged_df = merged_df.dropna()
print(merged_df.columns)
print(merged_df.shape)
print(merged_df.isnull().sum())
print(merged_df.dtypes)


merged_df.to_csv('../data/merged_data_raw.csv', index=False, encoding='utf-8')