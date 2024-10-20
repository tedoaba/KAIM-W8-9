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
        
    # Rename columns
    old_names = ['TransactionID', 'FraudIndicator', 'Category', 'TransactionAmount',
                 'AnomalyScore', 'Timestamp', 'MerchantID', 'Amount', 'CustomerID',
                 'Name', 'Age', 'Address', 'AccountBalance', 'LastLogin', 'SuspiciousFlag']
    new_names = ['TID', 'FI', 'Category', 'T_Amount', 'A_Score', 'TS', 'MID', 'Amount',
                 'CID', 'Name', 'Age', 'Address', 'Balance', 'Last_Login', 'Sus_Flag']

    new_column_names = dict(zip(old_names, new_names))
    data.rename(columns=new_column_names, inplace=True)

    # Write DataFrame to PostgreSQL table
    data.to_sql('features', engine, if_exists='replace', index=False)


    # Query the first 5 rows using pandas
    df = pd.read_sql('SELECT * FROM features LIMIT 15', engine)

    # Convert DataFrame to dictionary for template rendering
    features = df.to_dict(orient='records')

    return render_template('data/data.html', features=features)

@bp.route('/predict')
def train_model():
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise RuntimeError("DATABASE_URL environment variable not set.")
    
    engine = create_engine(database_url)
    
    # Fetch data from database
    df = pd.read_sql('SELECT * FROM features', engine)

    # Check if the DataFrame is empty
    if df.empty:
        return jsonify({"error": "No data available for training."}), 400
    
    # Initialize a LabelEncoder object
    label_encoder = LabelEncoder()

    # Iterate through each column in the dataframe
    for column in df.columns:
        # Check if the column datatype is not numeric
        if df[column].dtype not in ['int64', 'float64']:
            # Fit label encoder and transform values
            df[column] = label_encoder.fit_transform(df[column])
            
    # Separate features and target variable
    features = df.drop(columns=['FI'])
    target = df['FI']

    # Apply SMOTE
    smote = SMOTE(random_state=42)
    features_resampled, target_resampled = smote.fit_resample(features, target)

    # Combine resampled features and target into a DataFrame
    df = pd.concat([pd.DataFrame(features_resampled, columns=features.columns), pd.Series(target_resampled, name='FI')], axis=1)

    
    # Preprocess data
    target_column = 'FI'
    X = df.drop(columns=[target_column])
    y = df[target_column]
    
    y = pd.Series(y)
    
    # Get the numeric columns
    numeric_columns = X.select_dtypes(include=['number']).columns

    # Create the StandardScaler
    transform = preprocessing.StandardScaler()

    # Fit the scaler on the data (calculate mean and standard deviation)
    transform.fit(X[numeric_columns])

    # Transform the data using the fitted transform and reassign it to X
    X[numeric_columns] = transform.transform(X[numeric_columns])
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    model = XGBClassifier()
    model.fit(X_train, y_train)
    
    # Save model
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    # Make predictions on the testing data
    y_pred = model.predict(X_test)

    # Calculate and print various metrics to evaluate the best model's performance
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    confusion = confusion_matrix(y_test, y_pred)

    print("Best Model Evaluation Metrics:")
    print("Accuracy:", accuracy)
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1 Score:", f1)
    print("Confusion Matrix:")
    print(confusion)
    
    
    # Get feature importances
    importances = model.feature_importances_

    # Convert importances to percentages
    importances_percentage = 100.0 * (importances / importances.sum())

    # Print feature importances in percentage
    for i, (feature, importance) in enumerate(zip(X.columns, importances_percentage)):
        print(f"{feature}: {importance:.2f}%")
    
    feature_importances = [(feature, importance) for feature, importance in zip(X.columns, importances_percentage)]

    
    return render_template(
        'data/predict.html',
        accuracy=accuracy,
        precision=precision,
        recall=recall,
        f1=f1,
        confusion=confusion,
        feature_importances=feature_importances
    )

# Load the model
with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

@bp.route('/result')
def result():
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise RuntimeError("DATABASE_URL environment variable not set.")
    
    engine = create_engine(database_url)
    
    # Fetch data from database
    data = pd.read_sql("SELECT * FROM transactions ORDER BY ctid DESC LIMIT 1", engine)
    
    # Rename columns
    old_names = ['TransactionID', 'FraudIndicator', 'Category', 'TransactionAmount',
                'AnomalyScore', 'Timestamp', 'MerchantID', 'Amount', 'CustomerID',
                'Name', 'Age', 'Address', 'AccountBalance', 'LastLogin', 'SuspiciousFlag']
    new_names = ['TID', 'FI', 'Category', 'T_Amount', 'A_Score', 'TS', 'MID', 'Amount',
                'CID', 'Name', 'Age', 'Address', 'Balance', 'Last_Login', 'Sus_Flag']

    new_column_names = dict(zip(old_names, new_names))
    data.rename(columns=new_column_names, inplace=True)
    
    # print transaction ID
    #for ID in data['TID']:
     #   print("Transaction ID: ", ID)
    ID = data['TID']
    
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

    # Make prediction
    prediction = model.predict(df)
    print("Prediction: ", prediction)
    
    return render_template('data/result.html', prediction=prediction, ID=ID)