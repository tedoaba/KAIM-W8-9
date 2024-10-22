from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Transaction(db.Model):
    __tablename__ = 'transactions'

    user_id = db.Column(db.Integer, primary_key=True)
    signup_time = db.Column(db.DateTime, nullable=False)
    purchase_time = db.Column(db.DateTime, nullable=False)
    purchase_value = db.Column(db.Float, nullable=False)
    device_id = db.Column(db.String, nullable=False)
    source = db.Column(db.String, nullable=False)
    browser = db.Column(db.String, nullable=False)
    sex = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    ip_address = db.Column(db.Float, nullable=False)
    lower_bound_ip_address = db.Column(db.Float, nullable=False)
    upper_bound_ip_address = db.Column(db.Float, nullable=False)
    country = db.Column(db.String, nullable=False)

