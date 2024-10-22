from dash import Dash, dcc, html, Input, Output
import requests
import pandas as pd
import plotly.express as px

app = Dash(__name__, suppress_callback_exceptions=True)

# Layout of the dashboard
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),

    html.H1("Fraud Insights Dashboard"),
    
    # Summary Boxes
    html.Div(id='summary-boxes'),
    
    # Line chart for fraud trends
    dcc.Graph(id='fraud-trends-chart'),
    
    # Geographical analysis
    dcc.Graph(id='geographical-chart'),
    
    # Device and browser analysis
    dcc.Graph(id='device-browser-chart'),
])

# Callback to update summary boxes
@app.callback(Output('summary-boxes', 'children'),
              Input('url', 'pathname'))
def update_summary_boxes(pathname):
    response = requests.get('http://127.0.0.1:5000/api/summary')
    data = response.json()
    
    return html.Div([
        html.Div(f"Total Transactions: {data['total_transactions']}", style={'padding': 10}),
        html.Div(f"Total Fraud Cases: {data['total_fraud_cases']}", style={'padding': 10}),
        html.Div(f"Fraud Percentage: {data['fraud_percentage']:.2f}%", style={'padding': 10}),
    ])

# Callback to update fraud trends chart
@app.callback(Output('fraud-trends-chart', 'figure'),
              Input('url', 'pathname'))
def update_fraud_trends_chart(pathname):
    response = requests.get('http://127.0.0.1:5000/api/fraud_trends')
    data = pd.read_json(response.text)
    
    fig = px.line(data, x='purchase_time', y='fraud_cases', title='Fraud Cases Over Time')
    return fig

# Callback to update geographical analysis chart
@app.callback(Output('geographical-chart', 'figure'),
              Input('url', 'pathname'))
def update_geographical_chart(pathname):
    response = requests.get('http://127.0.0.1:5000/api/geographical_analysis')
    data = pd.read_json(response.text)
    
    fig = px.choropleth(data, locations='ip_address', locationmode='country',
                        color='country', title='Fraud Cases by Location')
    return fig

# Callback to update device and browser analysis chart
@app.callback(Output('device-browser-chart', 'figure'),
              Input('url', 'pathname'))
def update_device_browser_chart(pathname):
    response = requests.get('http://127.0.0.1:5000/api/device_browser_analysis')
    data = pd.read_json(response.text)
    
    fig = px.bar(data, x='device_id', y='class', color='browser',
                 title='Fraud Cases by Device and Browser')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
