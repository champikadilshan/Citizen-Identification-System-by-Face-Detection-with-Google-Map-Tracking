import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Initialize Firebase with your service account key
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendancerealtime-a89cc-default-rtdb.firebaseio.com/"
})

# Define your condition
x = 2  # Change this value as needed

if x > 1:
    # Use ipinfo.io to get your current location based on your IP address
    try:
        response = requests.get('https://ipinfo.io')
        location_info = response.json()

        # Parse the location data
        location = location_info.get('loc', '').split(',')
        if len(location) == 2:
            latitude, longitude = location
        else:
            raise ValueError("Invalid location data")

        # Get a reference to the Firebase Realtime Database
        ref = db.reference('Students')  # Change 'students' to your desired path

        # Student data
        student_id = "321654"
        student_data = {
            "name": "Jhon Smith",
            "major": "Data Science",
            "starting_year": 2021,
            "total_attendance": 6,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34",
            "location": {
                "latitude": latitude,
                "longitude": longitude
            }
        }

        # Update the student's data in the Firebase Realtime Database
        ref.child(student_id).set(student_data)

        print(f"Location data added to student {student_id}")
    except Exception as e:
        print(f"Error getting location: {str(e)}")
else:
    print("Condition x > 1 is not met. Location not sent.")
