from flask import Flask, request, jsonify

import pandas as pd
import mlflow
import mlflow.pyfunc
from mlflow.tracking import MlflowClient

client = MlflowClient()

registered_models = client.list_artifacts('09de7b0c3226470aa6fae393bc51e77c')

for model in registered_models:
    print(f"Model Name: {model.name}, Latest Version: {model.latest_version}, Stage: {model.latest_versions[0].current_stage}")


"""
app = Flask(__name__)

# Load the model
model_path = 'runs:/09de7b0c3226470aa6fae393bc51e77c/xgb_fraud_data'
model = mlflow.pyfunc.load_model(model_path)

@app.route('/predict', methods=['POST'])
def predict():
    # Get the data from the request
    data = request.get_json(force=True)
    # Convert data to DataFrame
    input_data = pd.DataFrame(data)
    
    # Make predictions
    predictions = model.predict(input_data)
    return jsonify(predictions.tolist())

if __name__ == '__main__':
    app.run(debug=True)
"""