from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Cấu hình kết nối database với SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/banking_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Khởi tạo SQLAlchemy
db = SQLAlchemy(app)

# Định nghĩa mô hình Customer
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Float, nullable=False)

# Định nghĩa mô hình Transaction
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)

@app.route('/')
def index():
    customers = Customer.query.all()
    return render_template('index.html', customers=customers)

@app.route('/create_customer', methods=['GET', 'POST'])
def create_customer():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        balance = float(request.form['balance'])
        
        new_customer = Customer(name=name, email=email, balance=balance)
        db.session.add(new_customer)
        db.session.commit()
        
        flash("Customer created successfully", "success")
        return redirect(url_for('index'))
    
    return render_template('create_customer.html')

@app.route('/transactions/<int:customer_id>', methods=['GET', 'POST'])
def transactions(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    
    if request.method == 'POST':
        transaction_type = request.form['transaction_type']
        amount = float(request.form['amount'])
        
        if transaction_type == 'deposit':
            customer.balance += amount
        elif transaction_type == 'withdraw':
            customer.balance -= amount
        
        new_transaction = Transaction(customer_id=customer_id, transaction_type=transaction_type, amount=amount)
        db.session.add(new_transaction)
        db.session.commit()
        
        flash("Transaction recorded successfully", "success")
        return redirect(url_for('index'))
    
    transactions = Transaction.query.filter_by(customer_id=customer_id).all()
    return render_template('transaction.html', transactions=transactions, customer_id=customer_id)

if __name__ == '__main__':
    app.run(debug=True)
