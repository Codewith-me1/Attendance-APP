import os
import datetime
import pyqrcode
import http.server
import socketserver

class Student:
    def __init__(self, id, name, roll_number, class_id):
        self.id = id
        self.name = name
        self.roll_number = roll_number
        self.class_id = class_id

class Class:
    def __init__(self, id, name, teacher_id):
        self.id = id
        self.name = name
        self.teacher_id = teacher_id

class Teacher:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Attendance:
    def __init__(self, student_id, class_id, attendance_timestamp):
        self.student_id = student_id
        self.class_id = class_id
        self.attendance_timestamp = attendance_timestamp

class QRCode:
    def __init__(self, class_id, qr_code_data, expiry_timestamp):
        self.class_id = class_id
        self.qr_code_data = qr_code_data
        self.expiry_timestamp = expiry_timestamp

students = []
classes = []
teachers = []
attendances = []
qr_codes = []

def generate_qr_code(class_id):
    qr_code_data = f"Class-{class_id}-{int(datetime.datetime.utcnow().timestamp())}"
    qr = QRCode(class_id=class_id, qr_code_data=qr_code_data, expiry_timestamp=datetime.datetime.utcnow() + datetime.timedelta(hours=12))
    qr_codes.append(qr)
    return qr_code_data

def mark_attendance(qr_code_data):
    parts = qr_code_data.split("-")
    class_id = int(parts[1])
    student_id = int(parts[2])

    qr_code = next((qr for qr in qr_codes if qr.class_id == class_id and qr.expiry_timestamp > datetime.datetime.utcnow()), None)
    if qr_code:
        attendance = Attendance(student_id=student_id, class_id=class_id, attendance_timestamp=datetime.datetime.utcnow())
        attendances.append(attendance)
        return "Attendance marked successfully!"
    else:
        return "Invalid QR code"

def start_server():
    PORT = 8000
    httpd = socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler)
    print(f"Serving at port {PORT}")
    httpd.serve_forever()

if __name__ == "__main__":
    # Initialize data
    students.append(Student(1, "John Doe", "12345", 1))
    classes.append(Class(1, "Math", 1))
    teachers.append(Teacher(1, "Mr. Smith"))

    # Generate initial QR code
    qr_code_data = generate_qr_code(1)

    # Create QR code HTML file
    with open("qr_code.html", "w") as f:
        f.write(f"""
            <!DOCTYPE html>
            <html>
              <head>
                <title>QR Code</title>
              </head>
              <body>
                <h1>QR Code</h1>
                <img src="https://chart.googleapis.com/chart?chs=200x200&cht=qr&chl={qr_code_data}" alt="QR Code">
              </body>
            </html>
        """)

    # Start server
    start_server()