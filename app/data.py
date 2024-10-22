import os
import pickle
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from flask import Blueprint, render_template, jsonify
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier
from sklearn import preprocessing
import mlflow
from mlflow import pyfunc
import xgboost as xgb


load_dotenv()

bp = Blueprint("data", __name__)

# Load the model
model = xgb.Booster()
model = model.load_model("model.xgb")

@bp.route("/data")
def data():
    # Retrieve database URL from environment variables
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise RuntimeError("DATABASE_URL environment variable not set.")

    # Create SQLAlchemy engine
    engine = create_engine(database_url)
    
    # Path to your CSV file
    CSV_FILE_PATH = os.path.join(os.path.dirname(__file__),'features.csv')

    # Load CSV into a DataFrame
    data = pd.read_csv(CSV_FILE_PATH)
    
    # Drop the first column if it exists
    if 'Unnamed: 0' in data.columns:
        data.drop(columns=['Unnamed: 0'], inplace=True)

    # Write DataFrame to PostgreSQL table
    data.to_sql('features', engine, if_exists='replace', index=False)


    # Query the first 5 rows using pandas
    df = pd.read_sql('SELECT * FROM features LIMIT 15', engine)

    # Convert DataFrame to dictionary for template rendering
    features = df.to_dict(orient='records')

    return render_template('data/data.html', features=features)

@bp.route('/result')
def result():
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise RuntimeError("DATABASE_URL environment variable not set.")
    
    engine = create_engine(database_url)
    
    # Fetch data from database
    data = pd.read_sql("SELECT * FROM transactions ORDER BY ctid DESC LIMIT 1", engine)
    
    ID = data['user_id']
    
    df = data
    
    # Initialize a LabelEncoder object
    label_encoder = LabelEncoder()

    # Iterate through each column in the dataframe
    for column in df.columns:
        # Check if the column datatype is not numeric
        if df[column].dtype not in ['int64', 'float64']:
            # Fit label encoder and transform values
            df[column] = label_encoder.fit_transform(df[column])
    
    # Get the numeric columns
    numeric_columns = df.select_dtypes(include=['number']).columns

    # Create the StandardScaler
    transform = preprocessing.StandardScaler()

    # Fit the scaler on the data (calculate mean and standard deviation)
    transform.fit(df[numeric_columns])

    # Transform the data using the fitted transform and reassign it to X
    df[numeric_columns] = transform.transform(df[numeric_columns])

    df = xgb.DMatrix(df)

    prediction = None

    if model is None:
        print("Model is not loaded. Please check the loading process.")
    else:
        prediction = model.predict(df)


    # Make prediction
    #prediction = model.predict(df)
    print("Prediction: ", prediction)
    
    return render_template('data/result.html', prediction=prediction, ID=ID)