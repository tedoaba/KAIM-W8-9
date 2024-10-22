import mlflow
# Predict on a Pandas DataFrame.
import pandas as pd

from mlflow import MlflowClient

client = MlflowClient()
client.create_registered_model("xgb_credit_data")

client = MlflowClient()
result = client.create_model_version(
    name="xgb_credit_data",
    source='mlartifacts/377415131768587313/cc1f15c2202b4dff854b81d2d968e4df/artifacts/model',
    run_id="cc1f15c2202b4dff854b81d2d968e4df",
)


#import pandas as pd

# Define the input values as a dictionary (as per your example)
input_values = {
    'Time': 0.0, 'V1': -1.359807, 'V2': -0.072781, 'V3': 2.536346, 
    'V4': 1.378155, 'V5': -0.338321, 'V6': 0.462388, 'V7': 0.239599, 
    'V8': 0.098698, 'V9': 0.363787, 'V10': 0.090794, 'V11': -0.551600, 
    'V12': -0.617801, 'V13': -0.991390, 'V14': -0.311169, 'V15': 1.468177, 
    'V16': -0.470401, 'V17': 0.207971, 'V18': 0.025791, 'V19': 0.403993, 
    'V20': 0.251412, 'V21': -0.018307, 'V22': 0.277838, 'V23': -0.110474, 
    'V24': 0.066928, 'V25': 0.128539, 'V26': -0.189115, 'V27': 0.133558, 
    'V28': -0.021053, 'Amount': 149.62
}

# Convert the dictionary to a Pandas DataFrame
input_df = pd.DataFrame([input_values])

# Display the DataFrame
print(input_df)

# Load model as a PyFuncModel.
loaded_model = mlflow.pyfunc.load_model(result)

loaded_model.predict(input_df)