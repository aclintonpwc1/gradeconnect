from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import random  
import pyodbc

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://PiedPiper:password123!@gradeconnect-server.database.windows.net/GradeConnect?driver=SQL+Server'  
db = SQLAlchemy(app)  
bcrypt = Bcrypt(app) 

class User(db.Model):  
    __tablename__ = 'facultyInfo1'
    facultyID = db.Column(db.Integer, primary_key=True, autoincrement=False)  
    userEmail = db.Column(db.String(50), unique=True, nullable=False)  
    userPassword = db.Column(db.String(1000), nullable=False)
    facultyRole = db.Column(db.String(50), nullable=False)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)

@app.route('/')
def home():
    if 'userEmail' in session:  
            return render_template('home.html', userEmail=session['userEmail'])  
    else:  
        return redirect(url_for('login')) 
@app.route('/admin')
def admin():  
    return render_template('admin.html')
@app.route('/course')
def course():  
    return render_template('course.html')
@app.route('/student')
def student():  
    return render_template('student.html')

@app.route('/login', methods=['GET', 'POST']) 
def login():  
    if request.method == 'POST':
        userEmail = request.form['userEmail']  
        userPassword = request.form['userPassword']  
    
        # Query the database for the user  
        user = User.query.filter_by(userEmail=userEmail).first() 
  
        if user and bcrypt.check_password_hash(user.userPassword, userPassword.encode('utf-8')):  
            session['userEmail'] = userEmail
            # User login successful, redirect to appropriate faculty view  
            if user.facultyRole == 'Admin':  
                return redirect(url_for('admin'))  
            elif user.facultyRole == 'Teacher':  
                return redirect(url_for('course-to-student'))  
            elif user.facultyRole == 'Exam Officer':  
                return redirect(url_for('examscore'))  
            # elif user.facultyRole == 'Principal':  
            #     return redirect(url_for('report'))  
            else:  
                return redirect(url_for('login'))
        else:  
            # Invalid credentials  
            flash('Invalid username or password', 'error')  
            return redirect(url_for('login'))  
    else:
        return render_template('home.html')  
    
# Route for user sign up  
@app.route('/signup', methods=['GET', 'POST'])  
def signUp():  
    if request.method == 'POST':
        facultyID =  random.randint(100000000, 999999999)
        userEmail = request.form['userEmail']  
        userPassword = request.form['userPassword']  
        facultyRole = request.form['facultyRole']  
        firstName = request.form['firstName']  
        lastName = request.form['lastName']  
        if request.form['facultyRole'] == 'Admin':
            facultyRole = request.form['facultyRole']
        elif request.form['facultyRole'] == 'Teacher':
            facultyRole = request.form['facultyRole']
        elif request.form['facultyRole'] == 'Exam Officer':
            facultyRole = request.form['facultyRole']
        elif request.form['facultyRole'] == 'Principal':
            facultyRole = request.form['facultyRole']
        else:
            return jsonify({'message': 'Need to select faculty role'})
        
  
        # Check if the username already exists  
        existing_user = User.query.filter_by(userEmail=userEmail).first()  
        if existing_user:  
            return jsonify({'message': 'Username already exists'})  
  
        # Create a new user  
        hashed_password = bcrypt.generate_password_hash(userPassword).decode('utf-8')  
        new_user = User(facultyID=facultyID, userEmail=userEmail, userPassword=hashed_password, facultyRole=facultyRole, firstName=firstName, lastName=lastName)  
        db.session.add(new_user)  
        db.session.commit()   
  
        #return jsonify({'message': 'User created successfully'}) 
        # Flash a success message  
        flash('User created successfully, please login', 'success')
        # Redirect the user to the login page  
        return redirect(url_for('login'))
  
    else:
        return render_template('signUp.html') 
    
# Route for user logout  
@app.route('/logout')  
def logout():  
    session.pop('userEmail', None)  
    return redirect(url_for('login'))  


conn = pyodbc.connect('Driver={SQL Server};'  
                          'Server=gradeconnect-server.database.windows.net;'  
                          'Database=GradeConnect;'  
                          'UID=PiedPiper;'  
                          'PWD=password123!;')  
cursor = conn.cursor()


"""
Admin Page
"""

# Adding a new course
@app.route('/course', methods=['GET','POST'])
def newCourse():
    if request.method == 'POST':
        courseName = request.form.get('courseName')

        cursor.execute("SELECT courseID FROM courseInfo")
        courseIDColumn = cursor.fetchall()

        courseID = random.randint(100000000, 999999999)
        count = 1
        while count > 0:
            count = 0
            for tuple in courseIDColumn:
                if tuple[0] == courseID:
                    courseID = random.randint(100000000, 999999999)

        cursor.execute("INSERT INTO courseInfo (courseID, courseName) VALUES (?, ?)", (courseID, courseName))

        conn.commit()
        return "Form submitted successfully"
    return render_template('course.html')

# Adding a new student
@app.route('/student', methods=['GET','POST'])
def newStudent():
    if request.method == 'POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        contact = request.form.get('contact')

        cursor.execute("SELECT studentID FROM studentInfo")
        studentIDColumn = cursor.fetchall()

        studentID = random.randint(100000000, 999999999)
        count = 1
        while count > 0:
            count = 0
            for tuple in studentIDColumn:
                if tuple[0] == studentID:
                    studentID = random.randint(100000000, 999999999)

        cursor.execute("INSERT INTO studentInfo (studentID, firstName, lastName, contactNumber) VALUES (?, ?, ?, ?)", (studentID, firstName, lastName, contact))
        conn.commit()
        return "Form submitted successfully"
    return render_template('student.html')

"""
Teacher Page
"""
# Assigning a student to a course
@app.route('/course-to-student', methods=['GET', 'POST'])
def assignCourse():
    if request.method == 'POST':
        studentName = request.form.get('students').split(',')
        cursor.execute("SELECT studentID FROM studentInfo where firstName = ? and lastName = ?", (studentName[0].strip(), studentName[1].strip()))
        studentID = cursor.fetchval()

        courseName = request.form.get('courses')
        cursor.execute("SELECT courseID FROM courseInfo where courseName = ?", (courseName))
        courseID = cursor.fetchval()

        cursor.execute("SELECT SCID FROM studentCourseInfo")
        scidColumn = cursor.fetchall()

        scid = random.randint(100000000, 999999999)
        count = 1
        while count > 0:
            count = 0
            for tuple in scidColumn:
                if tuple[0] == scid:
                    scid = random.randint(100000000, 999999999)
        
        cursor.execute("SELECT CONCAT(firstName, ', ', lastName) as fullName FROM studentInfo")
        studentNameDropDown = cursor.fetchall()
        studentNameDropDown = sorted([name[0] for name in studentNameDropDown])

        cursor.execute("SELECT courseName FROM courseInfo")
        courseNameDropDown = cursor.fetchall()
        courseNameDropDown = sorted([name[0] for name in courseNameDropDown])

        cursor.execute("INSERT INTO studentCourseInfo (SCID, studentID, courseID) VALUES (?, ?, ?)", (scid, studentID, courseID))
        conn.commit()
        return render_template('courseToStudent.html', students=studentNameDropDown, courses=courseNameDropDown)

    cursor.execute("SELECT CONCAT(firstName, ', ', lastName) as fullName FROM studentInfo")
    studentNameDropDown = cursor.fetchall()
    studentNameDropDown = sorted([name[0] for name in studentNameDropDown])

    cursor.execute("SELECT courseName FROM courseInfo")
    courseNameDropDown = cursor.fetchall()
    courseNameDropDown = sorted([name[0] for name in courseNameDropDown])
    return render_template('courseToStudent.html', students=studentNameDropDown, courses=courseNameDropDown)

"""
Exam officer Page
"""
@app.route('/examscore', methods=['GET', 'POST'])
def examGrading():
    if request.method == 'POST':
# Inserting scores
# Get studentID, courseID, examName, and grade from frontend

        studentID = 1
        courseID = 1
        examName = '???'
        grade = 0

        passingThreshold = 65

        cursor.execute("SELECT examID FROM exams")
        examIDColumn = cursor.fetchall()
        examID = random.randint(100000000, 999999999)
        count = 1
        while count > 0:
            count = 0
            for tuple in examIDColumn:
                if tuple[0] == examID:
                    examID = random.randint(100000000, 999999999)

        passOrFail = 'Pass' if grade > passingThreshold else 'Fail'

        #cursor.execute("INSERT INTO exams (examID, studentID, courseID, examName, grade, passOrFail) VALUES (?, ?, ?, ?, ?, ?)", (examID, studentID, courseID, examName, grade, passOrFail))
    
    cursor.execute("SELECT CONCAT(firstName, ' ', lastName) as fullName FROM studentInfo")
    studentNameDropDown = cursor.fetchall()
    studentNameDropDown = sorted([name[0] for name in studentNameDropDown])
    cursor.execute("SELECT courseName FROM courseInfo")
    courseNameDropDown = cursor.fetchall()
    courseNameDropDown = sorted([name[0] for name in courseNameDropDown])
    return render_template('examscore.html', courses=courseNameDropDown, students=studentNameDropDown)

  
if __name__ == '__main__':  
    app.run(debug=True)  