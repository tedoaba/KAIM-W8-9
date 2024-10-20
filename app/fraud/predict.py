from flask import Blueprint, render_template, send_file, request, jsonify
import matplotlib.pyplot as plt
from fraud.models import db, Transaction
import io
import pandas as pd
import pickle

from datetime import datetime, timezone
import pickle
from sklearn.preprocessing import LabelEncoder
import pandas as pd


bp = Blueprint("predict", __name__)


@bp.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    fig.savefig(output, format='png')
    output.seek(0)
    return send_file(output, mimetype='image/png')

def create_figure():
    # Sample data
    categories = ['TransactionID', 'Category', 'Amount', 'AnomalyScore', 'Timestamp']
    values = [30, 30, 15, 10, 20]

    fig, ax = plt.subplots()
    ax.bar(categories, values)
    ax.set_xlabel('Features')
    ax.set_ylabel('Importance (%)')
    ax.set_title('Feature Importance Visualization')

    return fig
