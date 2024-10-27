import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
from sqlalchemy import func
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

        fig = px.bar(device_browser_df, x='fraud_cases', y='device_id', color='browser', title='Fraud by Device and Browser')
        return fig

    return dash_app

def create_fraud_analysis_dash_app(flask_app, db):
    dash_app = Dash(__name__, external_stylesheets=["https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css"], server=flask_app, url_base_pathname='/fraud_analysis/')

    dash_app.layout = html.Div([
        html.H3('Adey Innovation Inc. Fraud Analysis Dashboard', className="text-2xl font-bold text-center mb-6"),

        # Summary Boxes
        html.Div([
            html.Div(id='total-transactions', className=' rounded-lg text-center p-4 w-48 shadow-md'),
            html.Div(id='total-fraud-cases', className=' rounded-lg text-center p-4 w-48 shadow-md'),
            html.Div(id='fraud-percentage', className=' rounded-lg text-center p-4 w-48 shadow-md'),
        ], className="flex gap-6 justify-center mb-8"),

        # Time Series Line Chart
        html.Div([
            dcc.Graph(id='fraud-time-series', className="rounded-lg")
        ], className="p-4 rounded-lg shadow-lg mb-8"),

        # Geographic Analysis
        html.Div([
            dcc.Graph(id='fraud-geographic-analysis', className=" rounded-lg")
        ], className="p-4 rounded-lg shadow-lg mb-8"),

        # Device and Browser Fraud Analysis
        html.Div([
            dcc.Graph(id='fraud-device-browser-bar-chart', className=" rounded-lg")
        ], className="p-4 rounded-lg shadow-lg "),

        # Fraud through time
        html.Div([
            dcc.Graph(id='hourly-fraud-graph', className="rounded-lg")
        ], className="p-4 rounded-lg shadow-lg mb-8"),

        html.Div([
            dcc.Graph(id='daily-fraud-graph', className="rounded-lg")
        ], className="p-4 rounded-lg shadow-lg mb-8"),

        html.Div([dcc.Graph(id='purchase-value-distribution', className="rounded-lg")
                  ], className="p-4 rounded-lg shadow-lg mb-8"),
        html.Div([dcc.Graph(id='user-age-distribution', className="rounded-lg")
                  ], className="p-4 rounded-lg shadow-lg mb-8"),
        html.Div([dcc.Graph(id='fraud-count-plot', className="rounded-lg")
                  ], className="p-4 rounded-lg shadow-lg mb-8")
    ], className="container mx-auto py-10")

    # Callback to update summary boxes
    @dash_app.callback(
        [Output('total-transactions', 'children'),
         Output('total-fraud-cases', 'children'),
         Output('fraud-percentage', 'children')],
        [Input('fraud-time-series', 'id')]  # Dummy input for initial load
    )
    def update_summary_boxes(_):
        with flask_app.app_context():
            total_transactions = db.session.query(func.count(Features.user_id)).scalar()
            total_fraud_cases = db.session.query(func.count(Features.class_)).filter(Features.class_ == 1).scalar()
            fraud_percentage = (total_fraud_cases / total_transactions * 100) if total_transactions else 0

        return (
            html.Div([
                html.P("Total Transactions", className="text-lg font-semibold text-gray-700"),
                html.P(f"{total_transactions}", className="text-2xl font-bold text-blue-600")
            ]),
            html.Div([
                html.P("Total Fraud Cases", className="text-lg font-semibold text-gray-700"),
                html.P(f"{total_fraud_cases}", className="text-2xl font-bold text-red-600")
            ]),
            html.Div([
                html.P("Fraud Percentage", className="text-lg font-semibold text-gray-700"),
                html.P(f"{fraud_percentage:.2f}%", className="text-2xl font-bold text-yellow-500")
            ])
        )

    # Callback for fraud time series chart
    @dash_app.callback(
        Output('fraud-time-series', 'figure'),
        [Input('fraud-time-series', 'id')]
    )
    def update_fraud_time_series(_):
        with flask_app.app_context():
            fraud_data = db.session.query(Features.purchase_time, Features.class_).filter(Features.class_ == 1).all()
            fraud_df = pd.DataFrame(fraud_data, columns=['purchase_time', 'class_'])
            fraud_df['purchase_time'] = pd.to_datetime(fraud_df['purchase_time'])
            fraud_df = fraud_df.set_index('purchase_time').resample('D').size().reset_index(name='fraud_cases')

        fig = px.line(fraud_df, x='purchase_time', y='fraud_cases', title='Detected Fraud Cases Over Time')
        fig.update_layout(xaxis_title="Date", yaxis_title="Number of Fraud Cases")
        return fig

    # Callback for geographic fraud analysis
    @dash_app.callback(
        Output('fraud-geographic-analysis', 'figure'),
        [Input('fraud-geographic-analysis', 'id')]
    )
    def update_fraud_geographic_analysis(_):
        with flask_app.app_context():
            fraud_geo_data = db.session.query(Features.country, func.count(Features.class_)).filter(Features.class_ == 1).group_by(Features.country).all()
            geo_df = pd.DataFrame(fraud_geo_data, columns=['country', 'fraud_cases'])

        fig = px.choropleth(geo_df, locations='country', locationmode='country names', color='fraud_cases',
                            title='Geographic Distribution of Fraud Cases',
                            color_continuous_scale='Reds')
        fig.update_layout(geo=dict(showframe=False, projection_type='natural earth'))
        return fig

    # Callback for device and browser fraud analysis
    @dash_app.callback(
        Output('fraud-device-browser-bar-chart', 'figure'),
        [Input('fraud-device-browser-bar-chart', 'id')]
    )
    def update_device_browser_fraud_analysis(_):
        with flask_app.app_context():
            device_browser_data = (
                db.session.query(Features.device_id, Features.browser, func.count(Features.class_))
                .filter(Features.class_ == 1)
                .group_by(Features.device_id, Features.browser)
                .all()
            )
            device_browser_df = pd.DataFrame(device_browser_data, columns=['device_id', 'browser', 'fraud_cases'])

        fig = px.bar(device_browser_df, x='device_id', y='fraud_cases', color='browser',
                     title='Fraud Cases by Device and Browser', barmode='group')
        fig.update_layout(xaxis_title="Device ID", yaxis_title="Number of Fraud Cases")
        return fig
    
    # Callback for fraud through time
    @dash_app.callback(
        Output('hourly-fraud-graph', 'figure'),
        Output('daily-fraud-graph', 'figure'),
        [Input('hourly-fraud-graph', 'id')]  # Dummy input for triggering
    )
    def update_time_based_analysis(_):
        with flask_app.app_context():
            # Query for time and class data from the database
            time_class_data = (
                db.session.query(Features.purchase_time, Features.class_)
                .all()
            )
            fraud_data = pd.DataFrame(time_class_data, columns=['purchase_time', 'class_'])
            fraud_data['purchase_time'] = pd.to_datetime(fraud_data['purchase_time'])
            fraud_data['hour_of_day'] = fraud_data['purchase_time'].dt.hour
            fraud_data['day_of_week'] = fraud_data['purchase_time'].dt.dayofweek

        # Create a histogram for transaction hour vs fraud class
        hourly_fig = px.histogram(fraud_data, x='hour_of_day', color='class_',
                                  title='Transaction Hour vs Fraud Class',
                                  labels={'hour_of_day': 'Hour of Day', 'class_': 'Fraud Class'},
                                  barmode='group')

        # Create a histogram for transaction day of week vs fraud class
        daily_fig = px.histogram(fraud_data, x='day_of_week', color='class_',
                                 title='Transaction Day of Week vs Fraud Class',
                                 labels={'day_of_week': 'Day of Week', 'class_': 'Fraud Class'},
                                 barmode='group')

        return hourly_fig, daily_fig
    

    # Callback for distribution of purchase values
    @dash_app.callback(
        Output('purchase-value-distribution', 'figure'),
        [Input('purchase-value-distribution', 'id')]  # Dummy input for initial load
    )
    def update_purchase_value_distribution(_):
        with flask_app.app_context():
            fraud_data = db.session.query(Features.purchase_value, Features.age, Features.class_).all()
            fraud_df = pd.DataFrame(fraud_data, columns=['purchase_value', 'age', 'class'])
        fig = px.histogram(fraud_df, x='purchase_value', nbins=50, title='Distribution of Purchase Values', 
                       marginal='rug', histnorm='probability density')
        return fig

    # Callback for distribution of user age
    @dash_app.callback(
        Output('user-age-distribution', 'figure'),
        [Input('user-age-distribution', 'id')]  # Dummy input for initial load
    )
    def update_user_age_distribution(_):
        with flask_app.app_context():
            fraud_data = db.session.query(Features.purchase_value, Features.age, Features.class_).all()
            fraud_df = pd.DataFrame(fraud_data, columns=['purchase_value', 'age', 'class'])
        fig = px.histogram(fraud_df, x='age', nbins=20, title='Distribution of User Age', 
                       marginal='rug', histnorm='probability density')
        return fig

    # Callback for fraud count plot
    @dash_app.callback(
        Output('fraud-count-plot', 'figure'),
        [Input('fraud-count-plot', 'id')]  # Dummy input for initial load
    )
    def update_fraud_count_plot(_):
        with flask_app.app_context():
            fraud_data = db.session.query(Features.purchase_value, Features.age, Features.class_).all()
            fraud_df = pd.DataFrame(fraud_data, columns=['purchase_value', 'age', 'class'])
        fig = px.histogram(fraud_df, x='class', color='class', title='Fraud vs Non-Fraud Transactions', 
                       category_orders={'class': [0, 1]})
        return fig

    return dash_app
