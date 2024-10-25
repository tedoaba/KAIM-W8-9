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

class Features(db.Model):
    __tablename__ = 'features'

    user_id = db.Column(db.Integer, primary_key=True)
    signup_time = db.Column(db.DateTime)
    purchase_time = db.Column(db.DateTime)
    purchase_value = db.Column(db.Float)
    device_id = db.Column(db.String)
    source = db.Column(db.String)
    browser = db.Column(db.String)
    sex = db.Column(db.String)
    age = db.Column(db.Integer)
    ip_address = db.Column(db.String)
    class_ = db.Column('class', db.Integer)  # Fraud class: 0 = non-fraud, 1 = fraud
    lower_bound_ip_address = db.Column(db.BigInteger)
    upper_bound_ip_address = db.Column(db.BigInteger)
    country = db.Column(db.String)
