from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///swift.db'
db = SQLAlchemy(app)

class Clients(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(80), nullable=False)
	last_name = db.Column(db.String(80), nullable=False)
	phone_number = db.Column(db.String(12), nullable=False)
	pin = db.Column(db.String(4), nullable=False)
	balance = db.Column(db.Integer, default = 0)
	datetime = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

class Agents(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(80), nullable=False)
	last_name = db.Column(db.String(80), nullable=False)
	phone_number = db.Column(db.String(12), nullable=False)
	pin = db.Column(db.String(12), nullable=False)
	balance = db.Column(db.Integer)
	datetime = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

class transaction_aprovals(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	phone_number = db.Column(db.Integer)
	details = db.Column(db.String(80), nullable=False)
	approved = db.Column(db.Boolean, default=0)
	datetime = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
	
class Transactions(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	from_id = db.Column(db.Integer)
	to_id = db.Column(db.Integer)
	details = db.Column(db.String(80), nullable=False)
	amount = db.Column(db.Integer)
	datetime = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

class client_withdraws(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	phone_number = db.Column(db.Integer)
	secrete_code = db.Column(db.Integer)
	amount = db.Column(db.Integer)
	datetime = db.Column(db.DateTime, default = datetime.utcnow)

class message(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	sender = db.Column(db.String(10))
	receiver = db.Column(db.String(10))
	content = db.Column(db.String(10))
	datetime = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
	seen = db.Column(db.Boolean(), nullable=False, default = 0)


if __name__ == '__main__':
	db.create_all()

