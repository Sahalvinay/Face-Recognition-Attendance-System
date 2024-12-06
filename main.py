import os
import pickle
import time
import csv
import numpy as np
import cvzone
import cv2
import face_recognition
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendancesystem-13141-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendancesystem-13141.appspot.com"
})

bucket = storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/background.png')

COL_NAMES = ['ID', 'TIME', 'SUBJECT', 'DAY', 'TEACHER', 'DURATION', 'STATUS', 'DATE']

folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
    # print(len(imgModeList))

    # load encoding
    # print("Loading Encoded File")
    file = open('EncodeFile.p', 'rb')
    encodeListKnownWithIds = pickle.load(file)
    file.close()
    encodeListKnown, studentIds = encodeListKnownWithIds
    # print(studentIds)
    # print("Encoded File Loaded")

    modeType = 0
    counter = 0
    id = -1
    imgStudent = []

while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    #attendace excel file

    ts = time.time()
    date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
    timestamp = datetime.fromtimestamp(ts).strftime("%H:%M:%S")
    day = datetime.fromtimestamp(ts).strftime("%A")
    hour = int(timestamp[:2])
    minute = int(timestamp[3:5])
    if day == "Monday" and hour >= 11 and hour < 13:
        subject = "AI"
        teacher = "PS"
        Duration = "11:15 to 1:15"
        if (hour == 11 and minute <= 30):
            status = "ON TIME"
        else:
            status = "YOU ARE LATE"
    elif day == "Monday" and hour >= 13 and hour < 16:
        subject = "CG"
        teacher = "LR"
        Duration = "1:15 to 4:15"
        if (hour == 13 and minute <= 30):
            status = "ON TIME"
        else:
            status = "YOU ARE LATE"
    elif day == "Tuesday" and hour >= 11 and hour < 13:
        subject = "CG"
        teacher = "LR"
        Duration = "11:15 to 1:15"
        if (hour == 11 and minute <= 30):
            status = "ON TIME"
        else:
            status = "YOU ARE LATE"
    elif day == "Tuesday" and hour >= 13 and hour < 15:
        subject = "AI"
        teacher = "PS"
        Duration = "1:15 to 3:15"
        if (hour == 13 and minute <= 30):
            status = "ON TIME"
        else:
            status = "YOU ARE LATE"
    elif day == "Tuesday" and hour >= 15 and hour < 17:
        subject = "DIP"
        teacher = "RS"
        Duration = "3:15 to 5:15"
        if (hour == 15 and minute <= 30):
            status = "ON TIME"
        else:
            status = "YOU ARE LATE"
    elif day == "Wednesday" and hour >= 10 and hour < 12:
        subject = "AI"
        teacher = "PS"
        Duration = "10:15 to 12:15"
        if (hour == 10 and minute <= 30):
            status = "ON TIME"
        else:
            status = "YOU ARE LATE"
    elif day == "Wednesday" and hour >= 12 and hour < 14:
        subject = "CG"
        teacher = "LR"
        Duration = "12:15 to 2:15"
        if (hour == 12 and minute <= 30):
            status = "ON TIME"
        else:
            status = "YOU ARE LATE"
    elif day == "Thursday" and hour >= 11 and hour < 13:
        subject = "AI"
        teacher = "PS"
        Duration = "11:15 to 1:15"
        if (hour == 11 and minute <= 35):
            status = "ON TIME"
        else:
            status = "YOU ARE LATE"
    elif day == "Thursday" and hour >= 13 and hour < 15:
        subject = "DSE6"
        Duration = "1:15 to 3:15"
        teacher = "DC"
        if (hour == 13 and minute <= 30):
            status = "ON TIME"
        else:
            status = "YOU ARE LATE"
    elif day == "Friday" and hour >= 12 and hour < 14:
        subject = "DIP"
        teacher = "RS"
        Duration = "12:15 to 2:15"
        if (hour == 12 and minute <= 30):
            status = "ON TIME"
        else:
            status = "YOU ARE LATE"
    else:
        subject = None
        teacher = None
        Duration = None
        status = None

    exist = os.path.isfile("C:/Users/VINAY SAHAL/PycharmProjects/FaceRecognition/Attendance.csv")
    attendance = [str(id), str(timestamp), str(subject), str(day), str(teacher), str(Duration), str(status), str(date)]
    # face recoginition starts
    if faceCurFrame:

        for encodeface, Faceloc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeface)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeface)
            # print("matches", matches)
            # print("faceDis", faceDis)

            matchIndex = np.argmin(faceDis)
            # print("match Index", matchIndex)

            if matches[matchIndex] and faceDis[matchIndex] < 0.45:
                # print("Known Face is Detected")
                # print(studentIds[matchIndex])
                y1, x2, y2, x1 = Faceloc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                id = studentIds[matchIndex]
                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                    cv2.imshow("Face Attendance", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1
            else:
                y1, x2, y2, x1 = Faceloc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                cv2.rectangle(imgBackground, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), (0, 0, 255), 2)
                cv2.putText(imgBackground, "Unknown Face", (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_PLAIN, 1,
                            (0, 0, 255), 2)
        # read images and student ids
        if counter != 0:

            if counter == 1:
                studentInfo = db.reference(f'Students/{id}').get()
                print(studentInfo)

                blob = bucket.get_blob(f'Images/{id}.png')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

                datetimeObject = datetime.strptime(studentInfo['Last_attendance_time'],
                                                   "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                print(secondsElapsed)

                if secondsElapsed > 30:
                    ref = db.reference(f'Students/{id}')
                    ref.child('Last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

                else:
                    modeType = 3
                    counter = 0
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

            if modeType != 3:

                if 10 < counter < 20:
                    modeType = 2

                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if counter <= 10:
                    cv2.putText(imgBackground, str(studentInfo['subject']), (1006, 550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.4, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(id), (1006, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['Semester']), (1006, 600),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 1)

                    (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv2.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                    imgBackground[175:175 + 216, 909:909 + 216] = imgStudent


                counter += 1

                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    else:
        modeType = 0
        counter - 0

    # cv2.imshow("Web Cam", img)
    cv2.imshow("Face Attendance", imgBackground)
    k = cv2.waitKey(1)


    if k == ord('o'):
        if exist:
            with open("C:/Users/VINAY SAHAL/PycharmProjects/FaceRecognition/Attendance.csv",
                      "a") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(attendance)
            csvfile.close()
        else:
            with open("C:/Users/VINAY SAHAL/PycharmProjects/FaceRecognition/Attendance.csv",
                      "a")  as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(COL_NAMES)
                writer.writerow(attendance)
            csvfile.close()
