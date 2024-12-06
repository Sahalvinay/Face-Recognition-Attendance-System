
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://faceattendancesystem-13141-default-rtdb.firebaseio.com/'
})

ref = db.reference('Students')

data = {
    "S119":
        {
            "name" : "Vinay Sahal",
            "subject" : "Computer Science",
            "Semester" : "6",

            "Last_attendance_time" : "2023-3-11 11:55:01"

        },
    "S106":
        {
            "name": "Ayush Kumar",
            "subject": "Computer Science",
            "Semester": "6",

            "Last_attendance_time": "2023-3-11 11:52:01"

        },
    "S127":
        {
            "name": "Ruchik Dey",
            "subject": "Computer Science",
            "Semester": "6",

            "Last_attendance_time": "2023-3-11 11:50:01"

        },
    "S108":
        {
            "name": "Pratik Chakroborty",
            "subject": "Computer Science",
            "Semester": "6",

            "Last_attendance_time": "2023-3-11 11:51:01"
        },
    "S078":
        {
            "name": "Niladri Banik",
            "subject": "Computer Science",
            "Semester": "6",

            "Last_attendance_time": "2023-3-11 11:52:01"
        },
    "S155":
        {
            "name": "Soumodeep Banerjee",
            "subject": "Computer Science",
            "Semester": "6",

            "Last_attendance_time": "2023-3-11 11:54:01"
        },
    "S049":
        {
            "name": "Animesh Sarkar",
            "subject": "Computer Science",
            "Semester": "6",

            "Last_attendance_time": "2023-3-11 11:53:01"
        },
    "S118":
        {
            "name": "Soumodeep Basu",
            "subject": "Computer Science",
            "Semester": "6",

            "Last_attendance_time": "2023-3-11 11:53:01"
        }
}

for key, value in data.items():
    ref.child(key).set(value)
