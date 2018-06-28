from flask import Flask, request, session, redirect, url_for, abort, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MySecRetKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookstore.db'

db=SQLAlchemy(app)
class Logindetails(db.Model):
	email=db.Column(db.String(100), primary_key=True)
	address=db.Column(db.String(100))
	username=db.Column(db.String(100))
	password=db.Column(db.String(100))

	def __init__(self,email,address,username,password):
		self.email=email
		self.address=address
		self.username=username
		self.password=password

	def __repr__(self):
		return self.email

class Cartdetails(db.Model):
	log = True
	id=db.Column(db.Integer, primary_key=True)
	email=db.Column(db.String(100), db.ForeignKey('logindetails.email'))
	image=db.Column(db.String(500))
	title=db.Column(db.String(500))
	quantity=db.Column(db.Integer)
	price=db.Column(db.Integer)

	def __init__(self,email,image,title,quantity,price):
		self.email=email
		self.image=image
		self.title=title
		self.quantity=quantity
		self.price=price

	def __repr__(self):
		return self.email

class Ordersummary(db.Model):
	log = True
	id=db.Column(db.Integer, primary_key=True)
	fullname=db.Column(db.String(100))
	email=db.Column(db.String(100), db.ForeignKey('logindetails.email'))	
	address=db.Column(db.String(500))
	city=db.Column(db.String(500))
	country=db.Column(db.String(500))
	pin=db.Column(db.Integer)
	image=db.Column(db.String(500))
	title=db.Column(db.String(500))
	quantity=db.Column(db.Integer)
	price=db.Column(db.Integer)	

	def __init__(self,fullname,email,address,city,country,pin,image,title,quantity,price):
		self.fullname=fullname
		self.email=email
		self.address=address
		self.city=city
		self.country=country
		self.pin=pin
		self.image=image
		self.title=title
		self.quantity=quantity
		self.price=price

	def __repr__(self):
		return self.email

db.create_all()

def authenticate(e,p):
	data=Logindetails.query.filter_by(email=e).filter_by(password=p).all()
	if len(data)>0:
		return True
	return False

def cartquantity(e,t,q):	
	data=Cartdetails.query.filter_by(title=t).filter_by(email=e).one()
	if int(data.quantity)+int(q)>3:
		return True	
	return False

with open("static/problem-solving-books.json") as data_file:
	data = json.loads(data_file.read())

@app.route('/')
def homepage():
	return render_template('homepage.html', size=len(data['items']), data=data, error="", cart="" )

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = ""
	cart = ""
	if request.method == 'POST':
		if authenticate(request.form['email'],request.form['password']):
			session['logged_in'] = True
			session['logged_email'] = request.form['email']
			Cartdetails.log = True			
			return redirect(url_for('homepage'))
		else:
			error = "Invalid Credentials"
	return render_template('login.html', error=error)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	error = None
	if request.method == 'POST':
		session['logged_in'] = True
		flash('You were logged in')
		newUser = Logindetails(email=request.form['email'],address=request.form['address'],username=request.form['username'],password=request.form['password'])
		db.session.add(newUser)
		db.session.commit()
		return render_template('login.html', error=error)
	return render_template('signup.html', error=error)

@app.route('/cart', methods=['GET', 'POST'])
def cart():
	error = ""
	cart = ""
	if request.method == 'POST':
		if session['logged_in'] == True:
			t=request.form['title']
			e=session['logged_email']
			q=request.form['quantity']
			p=request.form['price']			
			if len(Cartdetails.query.filter_by(title=t).filter_by(email=e).all())==0:
				newUser = Cartdetails(email=e,image=request.form['image'],title=t,quantity=q,price=p)
				db.session.add(newUser)
				db.session.commit()
				error = t+" added to cart"
			else:
				if cartquantity(e,t,q):
					error = "Cannot add more than 3 copies of the same book!"
				else:
					cartdata=Cartdetails.query.filter_by(title=t).filter_by(email=e).one()
					cartdata.quantity = str(int(cartdata.quantity)+int(q))	
					db.session.commit()
		return render_template('login.html', error="Please login to continue!")		
	return render_template('login.html', error=error)

@app.route('/deleteitem', methods=['GET', 'POST'])
def deleteitem():
	error = ""
	if request.method == 'POST':
		if session['logged_in'] == True:
			e=request.form['email']
			t=request.form['title']
			Cartdetails.query.filter_by(email=e).filter_by(title=t).delete() 
			db.session.commit()
			error = t+" removed from the cart"
	cart=Cartdetails.query.filter_by(email=e).all()
	session['cart']=len(cart)
	return render_template('homepage.html', size=len(data['items']), data=data, error=error, cart=cart)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
	email = ""
	if request.method == 'POST':
		if session['logged_in'] == True:
			email=session['logged_email']
	cart=Cartdetails.query.filter_by(email=email).all()
	return render_template('checkout.html', cart=cart)

@app.route('/myorders')
def myorders():
	order=""
	if session['logged_in'] == True:
		order=Ordersummary.query.filter_by(email=session['logged_email']).all()
	return render_template('orders.html', order=order)

@app.route('/summary', methods=['GET', 'POST'])
def summary():
	cart=Cartdetails.query.filter_by(email=session['logged_email']).all()
	if request.method == 'POST':
		if session['logged_in'] == True:
			email=session['logged_email']
			fullname=request.form['fullname']
			address=request.form['address']
			city=request.form['city']
			pin=request.form['pin']
			country=request.form['country']
			for c in cart:
				newUser = Ordersummary(fullname=fullname,email=email,address=address,city=city,country=country,pin=pin,image=c.image,title=c.title,quantity=c.quantity,price=c.price)
				db.session.add(newUser)
				db.session.commit()
			error="Order Placed Successfully"
			Cartdetails.query.filter_by(email=session['logged_email']).delete() 
			db.session.commit()
		else:
			error="There was some problem while placing your order. Please try again!"
	cart=Cartdetails.query.filter_by(email=session['logged_email']).all()
	session['cart']=len(cart)
	return render_template('homepage.html', size=len(data['items']), data=data, error=error, cart=cart)

@app.route('/logout')
def logout():
	session['logged_in'] = False
	Cartdetails.log = False
	return redirect(url_for('homepage'))

if __name__ == '__main__':
	app.run(debug=True)