import os
import pickle
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from flask import Blueprint, render_template
from sqlalchemy import create_engine

load_dotenv()

bp = Blueprint("data", __name__)

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
