import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
from sqlalchemy import create_engine, func
from app.models import Features 

def create_summary_dash_app(flask_app, db):
    dash_app = Dash(__name__, server=flask_app, url_base_pathname='/summary/')

    with flask_app.app_context():
        # Query for summary statistics from the 'features' table
        total_records = db.session.query(func.count(Features.user_id)).scalar()
        avg_purchase_value = db.session.query(func.avg(Features.purchase_value)).scalar()

    dash_app.layout = html.Div([
        html.H3('Summary Statistics'),
        html.P(f"Total Records: {total_records}"),
        html.P(f"Average Purchase Value: {avg_purchase_value:.2f}")
    ])

    return dash_app


def create_fraud_trends_dash_app(flask_app, db):
    dash_app = Dash(__name__, server=flask_app, url_base_pathname='/fraud_trends/')

    dash_app.layout = html.Div([
        html.H3('Fraud Trends Over Time'),
        dcc.Graph(id='fraud-trends-graph')
    ])

    @dash_app.callback(
        Output('fraud-trends-graph', 'figure'),
        [Input('fraud-trends-graph', 'id')]
    )
    def update_fraud_trends(_):
        with flask_app.app_context():
            # Query for fraud trends over time
            fraud_trends = (
                db.session.query(Features.purchase_time, func.count(Features.user_id).label('fraud_cases'))
                .filter(Features.class_ == 1)  # Assuming 'class' indicates fraud status
                .group_by(Features.purchase_time)
                .all()
            )
            fraud_trends_df = pd.DataFrame(fraud_trends, columns=['purchase_time', 'fraud_cases'])

        fig = px.line(fraud_trends_df, x='purchase_time', y='fraud_cases', title='Fraud Cases Over Time')
        return fig

    return dash_app


def create_geo_analysis_dash_app(flask_app, db):
    dash_app = Dash(__name__, server=flask_app, url_base_pathname='/geo_analysis/')

    dash_app.layout = html.Div([
        html.H3('Geographical Analysis of Fraud'),
        dcc.Graph(id='geo-analysis-graph')
    ])

    @dash_app.callback(
        Output('geo-analysis-graph', 'figure'),
        [Input('geo-analysis-graph', 'id')]
    )
    def update_geo_analysis(_):
        with flask_app.app_context():
            # Query for geographical fraud data
            geo_data = (
                db.session.query(Features.country, func.count(Features.ip_address).label('ip_address_count'))
                .group_by(Features.country)
                .all()
            )
            geo_data_df = pd.DataFrame(geo_data, columns=['country', 'ip_address_count'])

        fig = px.bar(geo_data_df, x='ip_address_count', y='country', title='Fraud Cases by Country')
        return fig

    return dash_app


def create_device_browser_dash_app(flask_app, db):
    dash_app = Dash(__name__, server=flask_app, url_base_pathname='/device_browser/')

    dash_app.layout = html.Div([
        html.H3('Device and Browser Analysis'),
        dcc.Graph(id='device-browser-graph')
    ])

    @dash_app.callback(
        Output('device-browser-graph', 'figure'),
        [Input('device-browser-graph', 'id')]
    )
    def update_device_browser_analysis(_):
        with flask_app.app_context():
            # Query for device and browser data
            device_browser_data = (
                db.session.query(Features.device_id, Features.browser, func.count(Features.class_).label('fraud_cases'))
                .filter(Features.class_ == 1)  # Assuming 'class' indicates fraud status
                .group_by(Features.device_id, Features.browser)
                .all()
            )
            device_browser_df = pd.DataFrame(device_browser_data, columns=['device_id', 'browser', 'fraud_cases'])

        fig = px.bar(device_browser_df, x='device_id', y='fraud_cases', color='browser', title='Fraud by Device and Browser')
        return fig

    return dash_app
