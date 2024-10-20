from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Transaction(db.Model):
    __tablename__ = 'transactions'

    TransactionID = db.Column(db.String, primary_key=True)
    Category = db.Column(db.String, nullable=False)
    TransactionAmount = db.Column(db.Float, nullable=False)
    AnomalyScore = db.Column(db.Float, nullable=False)
    Timestamp = db.Column(db.DateTime, default=lambda: datetime.now(tz=datetime.timezone.utc), nullable=False)
    MerchantID = db.Column(db.Integer, nullable=False)
    Amount = db.Column(db.Float, nullable=False)
    CustomerID = db.Column(db.Integer, nullable=False)
    Name = db.Column(db.String, nullable=False)
    Age = db.Column(db.Integer, nullable=False)
    Address = db.Column(db.String, nullable=False)
    AccountBalance = db.Column(db.Float, nullable=False)
    LastLogin = db.Column(db.DateTime, nullable=False)
    SuspiciousFlag = db.Column(db.Boolean, nullable=False)
