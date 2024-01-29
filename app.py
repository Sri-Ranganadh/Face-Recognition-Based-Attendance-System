from flask import Flask, render_template, request
import sqlite3
from datetime import datetime
import subprocess
import os

app = Flask(__name__)
 

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/register')
def register():
    return render_template('register.html')



@app.route('/register', methods=['POST'])
def submit_form():
    # Retrieve form data using the request object
    student_id = request.form.get('student_id').upper()
    name = request.form.get('name').upper()
    year = int(request.form.get('year'))
    section = request.form.get('section').upper()
    
    # Print or use the form data
    print("Student ID:", student_id)
    print("Name:", name)
    print("Year:", year)
    print("Section:", section)
    
    # Connect to the SQLite database
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    
    # Check if the StudentID already exists in the table
    cursor.execute("SELECT * FROM Students WHERE StudentID = ?", (student_id,))
    existing_student = cursor.fetchone()
    
    if existing_student:
        conn.close()
        message = os.path.join(script_dir, "message.py")
        subprocess.run(["python", message,"StudentID already exists! Please use a different ID."])
        return 
    else:
        # Insert the form data into the Students table
        cursor.execute("INSERT INTO Students (StudentID, Name, Year, Section) VALUES (?, ?, ?, ?)",
                       (student_id, name, year, section))
        
        # Commit the transaction and close the connection
        conn.commit()
        conn.close()
         
        script_dir = os.path.dirname(os.path.realpath(__file__))
        
        # Specify the path to get_faces_from_camera.py
        get_faces_script = os.path.join(script_dir, 'get_faces_from_camera_tkinter.py')
        print(get_faces_script)
        # Call the main() function from get_faces_from_camera.py using subprocess
        subprocess.run(["python", get_faces_script])

        message = os.path.join(script_dir, "message.py")
        subprocess.run(["python", message,"Student Registration Successful"])

        # train = os.path.join(script_dir, 'features_extraction_to_csv.py')
        # subprocess.run(["python",train])
        
        return render_template('register.html')

@app.route('/schedule')
def schedule():
    return render_template('schedule.html')
    
@app.route('/schedule', methods=['POST'])
def submit_schedule():
    # Retrieve form data using the request object
    subject_code = request.form.get('SubjectCode').upper()
    date = request.form.get('Date')
    subject_name = request.form.get('SubjectName').upper()
    shift = request.form.get('Shift').upper()
    
    # Connect to the SQLite database
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    
    # Check if the schedule already exists
    cursor.execute("SELECT * FROM Schedule WHERE SubjectCode = ? AND Date = ? AND Shift = ?",(subject_code, date, shift))
    existing_schedule = cursor.fetchone()
    
    if existing_schedule:
        conn.close()
        script_dir = os.path.dirname(os.path.realpath(__file__))
        message = os.path.join(script_dir, "take_attendance_popup.py")
        flag=subprocess.run(["python", message,"Schedule already exists!\nDo you want to take attendance?"])
        if(flag):
            take_attendance(subject_code, date, shift)
        else:
            return render_template('index.html')
    else:
        # Insert the form data into the Schedule table
        cursor.execute("INSERT INTO Schedule (SubjectCode, Date, SubjectName, Shift) VALUES (?, ?, ?, ?)",
                       (subject_code, date, subject_name, shift))
        
        # Commit the transaction and close the connection
        conn.commit()
        conn.close()
        script_dir = os.path.dirname(os.path.realpath(__file__))
        message = os.path.join(script_dir, "take_attendance_popup.py")
        flag=subprocess.run(["python", message,"Schedule registered successfully!\nDo you want to take attendance?"])
        if(flag):
            take_attendance(subject_code, date, shift)
        else:
            return render_template('index.html')
    return render_template('index.html')

def take_attendance(subject_code, date, shift):
    #redirecting it to attendance_taker.py by passing schedule-id
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    cursor.execute("SELECT ScheduleID FROM Schedule WHERE SubjectCode = ? AND Date = ? AND Shift = ?", (subject_code, date, shift))
    existing_schedule = cursor.fetchone()
    pass_id = existing_schedule[0]
    conn.close()
    script_dir = os.path.dirname(os.path.realpath(__file__))
    take = os.path.join(script_dir, "attendance_taker.py")
    subprocess.run(["python", take,str(pass_id)])
    return render_template('index.html')





if __name__ == '__main__':
    app.run(debug=True)
