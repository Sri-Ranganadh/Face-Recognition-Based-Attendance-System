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
    student_id = request.form.get('student_id')
    name = request.form.get('name')
    year = int(request.form.get('year'))
    section = request.form.get('section')
    
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

@app.route('/take-attendance')
def take_attendance():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    take = os.path.join(script_dir, "attendance_taker.py")
    subprocess.run(["python", take])
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
