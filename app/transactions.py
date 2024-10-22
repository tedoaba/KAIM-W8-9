from flask import Blueprint, render_template, redirect, request, url_for
from app.models import db, Transaction
from datetime import datetime, timezone

bp = Blueprint("transactions", __name__)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # Set the current time for signup_time and purchase_time if not provided
        signup_time = datetime.strptime(request.form['signup_time'], '%Y-%m-%dT%H:%M').replace(tzinfo=timezone.utc)
        purchase_time = datetime.strptime(request.form['purchase_time'], '%Y-%m-%dT%H:%M').replace(tzinfo=timezone.utc)
        
        transaction = Transaction(
            user_id=int(request.form['user_id']),
            signup_time=signup_time,
            purchase_time=purchase_time,
            purchase_value=float(request.form['purchase_value']),
            device_id=request.form['device_id'],
            source=request.form['source'],
            browser=request.form['browser'],
            sex=request.form['sex'],
            age=int(request.form['age']),
            ip_address=float(request.form['ip_address']),
            lower_bound_ip_address=float(request.form['lower_bound_ip_address']),
            upper_bound_ip_address=float(request.form['upper_bound_ip_address']),
            country=request.form['country']
        )
        db.session.add(transaction)
        db.session.commit()
        
        return redirect(url_for('transactions.history'))
    
    return render_template('transactions/create.html')

@bp.route('/history')
def history():
    transactions = Transaction.query.all()
    return render_template('transactions/history.html', transactions=transactions)
