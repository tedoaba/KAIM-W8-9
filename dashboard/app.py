from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# Load data
data_file = '../data/merged_data_raw.csv'
df = pd.read_csv(data_file)

@app.route('/')
def home():
    welcome = "Welcome"
    return welcome

@app.route('/api/summary', methods=['GET'])
def summary():
    total_transactions = len(df)
    total_fraud_cases = df[df['class'] == 1].shape[0]
    fraud_percentage = (total_fraud_cases / total_transactions) * 100 if total_transactions > 0 else 0
    return jsonify({
        'total_transactions': total_transactions,
        'total_fraud_cases': total_fraud_cases,
        'fraud_percentage': fraud_percentage
    })

@app.route('/api/fraud_trends', methods=['GET'])
def fraud_trends():
    # Group by date and count fraud cases
    trends = df[df['class'] == 1].groupby('purchase_time').size().reset_index(name='fraud_cases')
    return trends.to_json(orient='records')

@app.route('/api/geographical_analysis', methods=['GET'])
def geographical_analysis():
    geo_data = df.groupby('country')['ip_address'].sum().reset_index()
    return geo_data.to_json(orient='records')

@app.route('/api/device_browser_analysis', methods=['GET'])
def device_browser_analysis():
    device_browser_data = df.groupby(['device_id', 'browser'])['class'].sum().reset_index()
    return device_browser_data.to_json(orient='records')

if __name__ == '__main__':
    app.run(debug=True)
