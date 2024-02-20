from flask import Flask, request, jsonify, render_template, redirect, url_for, session 
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import pyodbc

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
    id = db.Column(db.Integer, primary_key=True)  
    username = db.Column(db.String(50), unique=True, nullable=False)  
    password = db.Column(db.String(50), nullable=False)

@app.route('/')
def home():
    if 'username' in session:  
            return render_template('home.html', username=session['username'])  
    else:  
        return redirect(url_for('login')) 

@app.route('/login', methods=['GET', 'POST']) 
def login():  
    if request.method == 'POST':
        username = request.form['username']  
        password = request.form['password']  
    
        # Query the database for the user  
        user = User.query.filter_by(username=username).first()  
  
        if user and bcrypt.check_password_hash(user.password, password):  
            session['username'] = username
            # User login successful  
            return jsonify({'message': 'Login successful'})  
        else:  
            # Invalid credentials  
            return jsonify({'message': 'Invalid username or password'})  

    return render_template('home.html')  
    
# Route for user sign up  
@app.route('/signup', methods=['GET', 'POST'])  
def signup():  
    if request.method == 'POST':  
        username = request.form['username']  
        password = request.form['password']  
  
        # Check if the username already exists  
        existing_user = User.query.filter_by(username=username).first()  
        if existing_user:  
            return jsonify({'message': 'Username already exists'})  
  
        # Create a new user  
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')  
        new_user = User(username=username, password=hashed_password)  
        db.session.add(new_user)  
        db.session.commit()  
  
        return jsonify({'message': 'User created successfully'})  
  
    return render_template('signUp.html') 
    
# Route for user logout  
@app.route('/logout')  
def logout():  
    session.pop('username', None)  
    return redirect(url_for('login'))  
  
if __name__ == '__main__':  
    app.run(debug=True)  