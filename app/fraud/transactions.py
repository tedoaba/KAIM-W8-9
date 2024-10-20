from flask import Blueprint, render_template, redirect, request, url_for
from fraud.models import db, Transaction
from datetime import datetime, timezone


bp = Blueprint("transactions", __name__)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # Set the current time for Timestamp if not provided
        timestamp = datetime.now(tz=timezone.utc)
        
        transaction = Transaction(
            TransactionID=request.form['TransactionID'],
            Category=request.form['Category'],
            TransactionAmount=float(request.form['TransactionAmount']),
            AnomalyScore=float(request.form['AnomalyScore']),
            Timestamp=timestamp,
            MerchantID=int(request.form['MerchantID']),
            Amount=float(request.form['Amount']),
            CustomerID=int(request.form['CustomerID']),
            Name=request.form['Name'],
            Age=int(request.form['Age']),
            Address=request.form['Address'],
            AccountBalance=float(request.form['AccountBalance']),
            LastLogin=datetime.strptime(request.form['LastLogin'], '%Y-%m-%dT%H:%M').replace(tzinfo=timezone.utc),
            SuspiciousFlag=bool(request.form.get('SuspiciousFlag'))
        )
        db.session.add(transaction)
        db.session.commit()
        
        return redirect(url_for('transactions.history'))
    
    return render_template('transactions/create.html')

@bp.route('/history')
def history():
    transactions = Transaction.query.all()
    return render_template('transactions/history.html', transactions=transactions)
