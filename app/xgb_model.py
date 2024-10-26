from flask import Blueprint, render_template
from flask import render_template
from sqlalchemy import create_engine
from sklearn.preprocessing import LabelEncoder, StandardScaler
import pandas as pd
import xgboost as xgb
import pickle
import os

bp = Blueprint("xgb_model", __name__)

@bp.route('/result')
def result():
    # Retrieve database URL from environment variables
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise RuntimeError("DATABASE_URL environment variable not set.")
    
    # Create a SQLAlchemy engine
    engine = create_engine(database_url)
    
    # Fetch data from the database
    try:
        data = pd.read_sql("SELECT * FROM transactions ORDER BY ctid DESC LIMIT 1", engine)
    except Exception as e:
        print(f"Error fetching data from database: {e}")
        return "Error fetching data from database.", 500

    # Extract user ID and prepare dataframe for preprocessing
    ID = data['user_id']
    df = data.copy()

    df['signup_time'] = pd.to_datetime(df['signup_time'])
    df['purchase_time'] = pd.to_datetime(df['purchase_time'])

    # Ensure 'ip_address' is treated as a string to handle missing values
    df['ip_address'] = df['ip_address'].astype(str)

    # Convert IP addresses to integer format, handling errors
    df['ip_address'] = df['ip_address'].apply(lambda x: convert_ip_to_int(x) if x != 'nan' else None)

    # Ensure both 'lower_bound_ip_address' and 'upper_bound_ip_address' in ip_data are strings
    df['lower_bound_ip_address'] = df['lower_bound_ip_address'].astype(str)
    df['upper_bound_ip_address'] = df['upper_bound_ip_address'].astype(str)

    # Convert the IP addresses in the IP-to-country dataset to integer format
    df['lower_bound_ip_address'] = df['lower_bound_ip_address'].apply(lambda x: convert_ip_to_int(x) if x != 'nan' else None)
    df['upper_bound_ip_address'] = df['upper_bound_ip_address'].apply(lambda x: convert_ip_to_int(x) if x != 'nan' else None)

    # Calculate transaction frequency and velocity
    df['signup_purchase_diff'] = (df['purchase_time'] - df['signup_time']).dt.total_seconds()

    # Calculate total transactions per user
    df['transaction_count'] = df.groupby('user_id')['user_id'].transform('count')

    # Extract hour of the day and day of the week
    df['hour_of_day'] = df['purchase_time'].dt.hour
    df['day_of_week'] = df['purchase_time'].dt.dayofweek

    # Normalize the transaction amount and signup_purchase_diff
    scaler = StandardScaler()
    df[['purchase_value', 'signup_purchase_diff']] = scaler.fit_transform(df[['purchase_value', 'signup_purchase_diff']])

    # Initialize a LabelEncoder object for encoding categorical data
    label_encoder = LabelEncoder()
    for col in ['source', 'browser', 'sex', 'country']:
        df[col] = label_encoder.fit_transform(df[col])

    # Load the model from pickle file
    pickle_file_path = os.path.join(os.path.dirname(__file__), '../models/xgb_model.pkl')
    if os.path.exists(pickle_file_path):
        with open(pickle_file_path, 'rb') as pickle_file:
            model = pickle.load(pickle_file)
    else:
        print(f"File not found: {pickle_file_path}")
        return "Model file not found.", 500

    # Check if model is loaded
    if model is None:
        print("Model is not loaded. Please check the loading process.")
        return "Model not loaded. Please check the setup.", 500
    
    # Prepare data for prediction using DMatrix
    feature_cols = ['user_id', 'purchase_value', 'source', 'browser', 'sex', 'age', 'ip_address',
       'lower_bound_ip_address', 'upper_bound_ip_address', 'country',
       'signup_purchase_diff', 'transaction_count', 'hour_of_day',
       'day_of_week']
    
    # Convert the DataFrame to a NumPy array for prediction
    feature_data = df[feature_cols].to_numpy()

    # Make predictions
    try:
        prediction = model.predict(feature_data)
        print("Prediction:", prediction)
    except Exception as e:
        print(f"Error during model prediction: {e}")
        return "Error during model prediction.", 500

    # Render result template with prediction
    return render_template('data/result.html', prediction=prediction, ID=ID)

def convert_ip_to_int(ip_address):
    try:
        # Ensure IP address is a valid string before conversion
        if isinstance(ip_address, str):
            return int(ip_address.replace('.', ''))
        else:
            return None
    except Exception as e:
        print(f"Error converting IP address {ip_address}: {e}")
        return None
