import os
import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime
import time
import webbrowser
####
import requests

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendancerealtime-a89cc-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendancerealtime-a89cc.appspot.com"
})

location = None

bucket = storage.bucket()

cap = cv2.VideoCapture(2)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/background.png')

# importing the mode images into a list
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))

# Load the encoding file
print("Loading Encoded File...")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
print("Encoded file Loaded")

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

    if faceCurFrame:

        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                id = studentIds[matchIndex]

                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                    cv2.imshow("Face Attendance", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1 #profile background

                    ###
                    #Show the locatiom

                    ###

        if counter != 0:

            if counter == 1:
                studentInfo = db.reference(f'Students/{id}').get()
                print(studentInfo)
                blob = bucket.get_blob(f'Images/{id}.png')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

                datetimeObject = datetime.strptime(studentInfo['last_seen_time'], "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                print(secondsElapsed)
                if secondsElapsed > 1:
                    ref = db.reference(f'Students/{id}')
                    studentInfo['total_caught'] += 1
                    ref.child('total_caught').set(studentInfo['total_caught'])
                    ref.child('last_seen_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    ref.child('caught').set(1)

                    ####
                    student_id = ref

                    # Use ipinfo.io to get your current location based on your IP address
                    try:
                        response = requests.get('https://ipinfo.io')
                        location_info = response.json()

                        # Parse the location data
                        location = location_info.get('loc', '').split(',')
                        if len(location) != 2:
                            raise ValueError("Invalid location data")
                    except Exception as e:
                        print(f"Error getting location: {str(e)}")

                    if location:
                        # Get a reference to the Firebase Realtime Database
                        ref = db.reference(
                            f'Students/{id}/location')  # Update only the location for the specific student

                        # Create a dictionary with the new location data
                        latitude, longitude = location
                        new_location = {
                            "latitude": latitude,
                            "longitude": longitude
                        }

                        # Update the location in the Firebase Realtime Database
                        ref.set(new_location)

                        print(f"Real-time location updated for student {student_id}")
                    else:
                        print("Location not updated due to an error in location retrieval.")



                else:
                    modeType = 3 #already marked banner
                    counter = 0
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

            if modeType != 3:

                if 10 < counter < 20:
                    modeType = 2 #makred completed banner


                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if counter <= 10:
                    cv2.putText(imgBackground, str(studentInfo['total_caught']), (861, 125),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['offence']), (1006, 550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(id), (1006, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentInfo['firstcase_year']), (1125, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                    (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv2.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                    imgBackground[175:175 + 216, 909:909 + 216] = imgStudent
                    time.sleep(1) #added to slow down the process

                counter += 1

                if counter >= 20:
                    counter = 0
                    modeType = 0 #scan your face
                    studentInfo = []
                    imgStudent = []
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    else:
        modeType = 0
        counter = 0

    cv2.imshow("Face Attendance", imgBackground)

    key = cv2.waitKey(1)
    if key == 27:  # Check for the "Esc" key (ASCII code 27)
        break


# Release the video capture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
