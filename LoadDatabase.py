import pandas as pd  
import numpy as np
import random  
import string  

# from flask import Flask, request
from flask_bcrypt import Bcrypt
import pyodbc
# app = Flask(__name__)
# @app.route('/insert', methods=['POST'])  
conn = pyodbc.connect('Driver={SQL Server};'  
                          'Server=gradeconnect-server.database.windows.net;'  
                          'Database=Grade Connect;'  
                          'UID=PiedPiper;'  
                          'PWD=password123!;')  

cursor = conn.cursor()
  
# Generate a unique 9-digit faculty ID for each row  
facultyIDs = random.sample(range(100000000, 999999999), 10)  
   
# Generate dummy first and last names  
firstNames = ['John', 'Jane', 'Michael', 'Emily', 'William', 'Olivia', 'James', 'Sophia', 'Benjamin', 'Isabella']  
lastNames = ['Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Miller', 'Wilson', 'Moore', 'Taylor']  

# Generate usernames using the first initial and full last name 
usernames = [f"{fname[0].lower()}{lname.lower()}" for fname, lname in zip(firstNames, lastNames)]
  
# Generate random passwords with 15 characters  
passwords = [''.join(random.choices(string.ascii_letters + string.digits, k=15)) for _ in range(10)] 
hashedPasswords =  [Bcrypt.generate_password_hash(password).decode('utf-8') for password in passwords]
passwords
for password in passwords:
    hashedPasswords =  Bcrypt.generate_password_hash(password).decode('utf-8')

Bcrypt.generate_password_hash('mfmkb').decode('utf-8')

# Generate roles, ensuring 'Principal' occurs only once  
roles = ['Admin', 'Teacher', 'Exam Officer']*3
roles.append('Principal')
random.shuffle(roles)

courseIDs = random.sample(range(100000000, 999999999), 8)
courseNames = ['MATH101', 'MATH201', 'MATH301', 'MATH401', 'SCI101', 'SCI201', 'SCI301', 'SCI401']

studentIDs = random.sample(range(100000000, 999999999), 5)

studFirstNames = ['Ken', 'Sam', 'John', 'Elizabeth', 'Jen']
studLastNames = ['James', 'Martin', 'Jackson', 'White', 'Black']

def generate_phone_number():  
    area_code = 917  
    first_three_digits = random.randint(100, 999)  
    last_four_digits = random.randint(1000, 9999)  
    return f"({area_code}) {first_three_digits}-{last_four_digits}"  
  
contactNumbers = []  
for _ in range(5):  
    contactNumbers.append(generate_phone_number())  
len(contactNumbers[0]) 

scids = random.sample(range(100000000, 999999999), 10)

for n in range(len(facultyIDs)):
    values = (facultyIDs[n], usernames[n], hashedPasswords[n], roles[n], firstNames[n], lastNames[n])  
    cursor.execute("INSERT INTO facultyInfo (facultyID, username, userPassword, facultyRole, firstName, lastName) VALUES (?, ?, ?, ?, ?, ?)", values)

for n in range(len(facultyIDs)):
    values = (facultyIDs[n], usernames[n], passwords[n], roles[n], firstNames[n], lastNames[n])  
    cursor.execute("INSERT INTO facultyInfo1 (facultyID, username, userPassword, facultyRole, firstName, lastName) VALUES (?, ?, ?, ?, ?, ?)", values)

"""
for n in range(len(courseIDs)):
    values = (courseIDs[n], courseNames[n])
    cursor.execute("INSERT INTO courseInfo (courseID, courseName) VALUES (?, ?)", values)
"""


"""
for n in range(len(studentIDs)):
    values = (studentIDs[n], firstNames[n], lastNames[n], contactNumbers[n])  
    cursor.execute("INSERT INTO studentInfo (studentID, firstName, lastName, contactNumber) VALUES (?, ?, ?, ?)"
                   , values)
"""
    
for n in range(len(studentIDs)):
    values1 = (scids[n], studentIDs[n], courseIDs[0])
    values2 = (scids[n+5], studentIDs[n], courseIDs[4])
    cursor.execute("INSERT INTO studentCourseInfo (SCID, studentID, courseID) VALUES (?, ?, ?)", values1)
    cursor.execute("INSERT INTO studentCourseInfo (SCID, studentID, courseID) VALUES (?, ?, ?)", values2)

cursor.execute("EXEC sp_rename 'facultyInfo.username', 'userEmail', 'COLUMN'") 
cursor.execute("UPDATE facultyInfo SET userEmail = userEmail || '@westrush.edu'") 
test = cursor.execute("SELECT userEmail from facultyInfo")

conn.commit()
cursor.close()
conn.close()