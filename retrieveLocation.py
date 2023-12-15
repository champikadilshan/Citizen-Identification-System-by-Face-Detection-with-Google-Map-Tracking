import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import webbrowser

# Initialize Firebase with your service account key
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendancerealtime-a89cc-default-rtdb.firebaseio.com/"
})

# Define the student's ID you want to retrieve location data for
student_id = "123456"  # Replace with the actual student ID

# Get a reference to the Firebase Realtime Database
ref = db.reference('Students')  # Change 'students' to your desired path

# Retrieve the location data for the specified student
student_location = ref.child(student_id).child("location").get()

if student_location:
    latitude = student_location.get("latitude")
    longitude = student_location.get("longitude")

    if latitude is not None and longitude is not None:
        print(f"Location data for student {student_id}: Latitude {latitude}, Longitude {longitude}")

        # Construct a Google Maps URL
        google_maps_url = f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"

        # Open the location in a web browser
        webbrowser.open(google_maps_url)
    else:
        print(f"Latitude or Longitude data missing for student {student_id}")
else:
    print(f"Student {student_id} not found in the database or location data is missing.")
