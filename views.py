from flask import Flask, render_template, request
import pyodbc
import random

"""
Admin Page
"""

app = Flask(__name__)
@app.route('/submit', methods=['GET','POST'])
def newCourse():
    if request.method == 'POST':
        courseName = request.form.get('courseName')
        facultyID = request.form.get('facultyID')
        conn = pyodbc.connect('Driver={SQL Server};'  
                          'Server=gradeconnect-server.database.windows.net;'  
                          'Database=Grade Connect;'  
                          'UID=PiedPiper;'  
                          'PWD=password123!;')  
        cursor = conn.cursor()

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

        cursor.execute("SELECT FCID FROM facultyCourseInfo")
        fcidColumn = cursor.fetchall()

        fcid = random.randint(100000000, 999999999)
        count = 1
        while count > 0:
            count = 0
            for tuple in fcidColumn:
                if tuple[0] == fcid:
                    fcid = random.randint(100000000, 999999999)

        cursor.execute("INSERT INTO courseInfo (FCID, courseID, facultyID) VALUES (?, ?, ?)", (fcid, courseID, facultyID))
        return "Form submitted successfully"
    return render_template('home.html')
if __name__ == '__main__':
    app.run()
# Retrieve coursename from frontend as courseName (and subject as subject?)
courseName = '???'
subject = '???'


# Get first name as firstName, last name as lastName, and contact number as contact
firstName = '???'
lastName = '???'
contact = '???'

import pyodbc
import random
conn = pyodbc.connect('Driver={SQL Server};'  
                          'Server=gradeconnect-server.database.windows.net;'  
                          'Database=Grade Connect;'  
                          'UID=PiedPiper;'  
                          'PWD=password123!;')  
cursor = conn.cursor()

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


"""
Teacher Page
"""

# Get course ID as courseID and student ID as studentID
courseID = '???'
studentID = '???'

import pyodbc
import random
conn = pyodbc.connect('Driver={SQL Server};'  
                          'Server=gradeconnect-server.database.windows.net;'  
                          'Database=Grade Connect;'  
                          'UID=PiedPiper;'  
                          'PWD=password123!;')  
cursor = conn.cursor()

cursor.execute("SELECT SCID FROM studentCourseInfo")
scidColumn = cursor.fetchall()

scid = random.randint(100000000, 999999999)
count = 1
while count > 0:
    count = 0
    for tuple in scidColumn:
        if tuple[0] == scid:
            scid = random.randint(100000000, 999999999)

cursor.execute("INSERT INTO courseInfo (courseID, courseName) VALUES (?, ?, ?)", (scid, studentID, courseID))

"""
Exam officer Page
"""

# Get studentID, courseID, examName, and grade from frontend

studentID = '???'
courseID = '???'
examName = '???'
grade = 0

passingThreshold = 65

import pyodbc
import random
conn = pyodbc.connect('Driver={SQL Server};'  
                          'Server=gradeconnect-server.database.windows.net;'  
                          'Database=Grade Connect;'  
                          'UID=PiedPiper;'  
                          'PWD=password123!;')  
cursor = conn.cursor()

cursor.execute("SELECT examID FROM examInfo")
examIDColumn = cursor.fetchall()
examID = random.randint(100000000, 999999999)
count = 1
while count > 0:
    count = 0
    for tuple in examIDColumn:
        if tuple[0] == examID:
            examID = random.randint(100000000, 999999999)

passOrFail = 'Pass' if grade > passingThreshold else 'Fail'

cursor.execute("INSERT INTO examInfo (examID, studentID, courseID, examName, grade, passOrFail) VALUES (examID, studentID, courseID, examName, grade, passOrFail)", (scid, studentID, courseID))