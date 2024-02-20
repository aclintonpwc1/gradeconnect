from flask import Flask, request, jsonify, render_template, redirect, url_for, session 
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
#import pyodbc

"""
conn = pyodbc.connect('Driver={SQL Server};'  
                          'Server=gradeconnect-server.database.windows.net;'  
                          'Database=Grade Connect;'  
                          'UID=PiedPiper;'  
                          'PWD=password123!;')  
 
cursor = conn.cursor()
"""

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://PiedPiper:password123!@gradeconnect-server.database.windows.net/Grade Connect?driver=SQL+Server'  
db = SQLAlchemy(app)  
bcrypt = Bcrypt(app) 

class User(db.Model):  
    __tablename__ = 'facultyInfo'
    id = db.Column(db.Integer, primary_key=True)  
    userEmail = db.Column(db.String(50), unique=True, nullable=False)  
    userPassword = db.Column(db.String(50), nullable=False)
    facultyRole = db.Column(db.String(50), nullable=True)
    firstName = db.Column(db.String(50), nullable=True)
    lastName = db.Column(db.String(50), nullable=True)

@app.route('/')
def home():
    if 'userEmail' in session:  
            return render_template('home.html', userEmail=session['userEmail'])  
    else:  
        return redirect(url_for('login')) 

@app.route('/login', methods=['GET', 'POST']) 
def login():  
    if request.method == 'POST':
        userEmail = request.form['userEmail']  
        userPassword = request.form['userPassword']  
    
        # Query the database for the user  
        user = User.query.filter_by(userEmail=userEmail).first()  
  
        if user and bcrypt.check_password_hash(user.userPassword, userPassword):  
            session['userEmail'] = userEmail
            # User login successful  
            return jsonify({'message': 'Login successful'})  
        else:  
            # Invalid credentials  
            return jsonify({'message': 'Invalid username or password'})  
    else:
        return render_template('home.html')  
    
# Route for user sign up  
@app.route('/signup', methods=['GET', 'POST'])  
def signUp():  
    if request.method == 'POST':  
        userEmail = request.form['userEmail']  
        userPassword = request.form['userPassword']  
  
        # Check if the username already exists  
        existing_user = User.query.filter_by(userEmail=userEmail).first()  
        if existing_user:  
            return jsonify({'message': 'Username already exists'})  
  
        # Create a new user  
        hashed_password = bcrypt.generate_password_hash(userPassword).decode('utf-8')  
        new_user = User(userEmail=userEmail, password=hashed_password)  
        db.session.add(new_user)  
        db.session.commit()  
  
        return jsonify({'message': 'User created successfully'})  
  
    else:
        return render_template('signUp.html') 
    
# Route for user logout  
@app.route('/logout')  
def logout():  
    session.pop('userEmail', None)  
    return redirect(url_for('login'))  
  
if __name__ == '__main__':  
    app.run(debug=True)  