from flask import Flask, render_template, request, jsonify
import pyodbc
import random
app = Flask(__name__)
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
@app.route('/examscores', methods=['GET', 'POST'])
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

        cursor.execute("INSERT INTO exams (examID, studentID, courseID, examName, grade, passOrFail) VALUES (?, ?, ?, ?, ?, ?)", (examID, studentID, courseID, examName, grade, passOrFail))
    
    cursor.execute("SELECT courseName FROM courseInfo")
    courseNameDropDown = cursor.fetchall()
    courseNameDropDown = sorted([name[0] for name in courseNameDropDown])
    return render_template('examscore.html', courses=courseNameDropDown)


if __name__ == '__main__':
    app.run(debug=True)