from flask import Flask, request, jsonify, render_template
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
    return render_template('home.html')

@app.route('/login', methods=['POST']) 
def login():  
    username = request.form['username']  
    password = request.form['password']  
  
    # Query the database for the user  
    user = User.query.filter_by(username=username).first()  
  
    if user and bcrypt.check_password_hash(user.password, password):  
        # User login successful  
        return jsonify({'message': 'Login successful'})  
    else:  
        # Invalid credentials  
        return jsonify({'message': 'Invalid username or password'})  
  
if __name__ == '__main__':  
    app.run(debug=True)  

"""
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    # Replace with your authentication logic
    if username == 'user' and password == 'password':
        session['username'] = username  # Set a session variable
        return jsonify(message='Login successful'), 200
    else:
        return jsonify(message='Login failed'), 401
    
@app.route('/logout', methods=['POST'])

def logout():
    session.pop('username', None)  # Clear the session variable
    return jsonify(message='Logged out'), 200

@app.route('/protected', methods=['GET'])

def protected():
    if 'username' in session:
        return jsonify(message='Protected data'), 200
    else:
        return jsonify(message='Unauthorized access'), 401
if __name__ == '__main__':
    app.run(debug=True, port=5000)

"""