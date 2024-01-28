import sqlite3
import subprocess
import os
# Connect to the database or create it if it doesn't exist
conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

# Create Students table
cursor.execute('''CREATE TABLE IF NOT EXISTS Students (
                    StudentID TEXT PRIMARY KEY,
                    Name TEXT,
                    Year INTEGER,
                    Section TEXT
                )''')

# Create Schedule table
cursor.execute('''CREATE TABLE IF NOT EXISTS Schedule (
                    ScheduleID INTEGER PRIMARY KEY,
                    SubjectCode TEXT,
                    Date DATE,
                    SubjectName TEXT,
                    Shift TEXT
                )''')

# Create Attendance table
cursor.execute('''CREATE TABLE IF NOT EXISTS Attendance (
                    AttendanceID INTEGER PRIMARY KEY,
                    StudentID INTEGER,
                    ScheduleID INTEGER,
                    Date DATE,
                    InTime TEXT,
                    OutTime TEXT,
                    FOREIGN KEY(StudentID) REFERENCES Students(StudentID),
                    FOREIGN KEY(ScheduleID) REFERENCES Schedule(ScheduleID)
                )''')

# Commit changes and close the connection
conn.commit()
conn.close()
script_dir = os.path.dirname(os.path.realpath(__file__))
message = os.path.join(script_dir, "message.py")
subprocess.run(["python", message,"Tables created successfully in attendance.db"])
print("Tables created successfully in attendance.db")
