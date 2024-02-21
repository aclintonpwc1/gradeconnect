from flask import Flask, render_template, request
import pyodbc
import os 
app = Flask(__name__)
@app.route('/submit', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('inputEmail3')
        password = request.form.get('inputPassword3')
        return "Form submitted successfully"
    return render_template('home.html')
if __name__ == '__main__':
    app.run()
    
conn = pyodbc.connect('Driver={SQL Server};'  
                          'Server=gradeconnect-server.database.windows.net;'  
                          'Database=GradeConnect;'  
                          'UID=PiedPiper;'  
                          'PWD=password123!;')  

cursor = conn.cursor()

cursor.execute("SELECT facultyRole FROM facultyInfo WHERE facultyID = ???")
role = cursor.fetchone()[0]

if role == 'Principal':
    view = "C:/Users/rchhabra023/Documents/Python Scripts/capstoneProject/Grade-Connect-amankwah-clinton/HTML/home.html"
elif role == 'Admin':
    view = '???'
elif role == 'Teacher':
    view = '???'
elif role == 'Exam Officer':
    view = '???'
else:
    view = "Take to error page?"

view = "C:/Users/rchhabra023/Documents/Python Scripts/capstoneProject/Grade-Connect-amankwah-clinton/HTML/home.html"
os.startfile(view)