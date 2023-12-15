import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://faceattendancerealtime-a89cc-default-rtdb.firebaseio.com/"
})

ref  = db.reference('Students')

data = {
    "321654":
        {
            "name": "Jhonx Smith",
            "offence": "Data Science",
            "firstcase_year": 2021,
            "total_caught": 33,
            "standing": "G",
            "year": 4,
            "last_seen_time": "2022-12-11 00:54:34",
            "caught": 0
        },
    "852741":
        {
            "name": "Emly Blunt",
            "offence": "Economics",
            "firstcase_year": 2021,
            "total_caught": 12,
            "standing": "B",
            "year": 1,
            "last_seen_time": "2022-12-11 00:54:34",
            "caught": 0
        },
    "963852":
        {
            "name": "Elon Musk",
            "offence": "Business",
            "firstcase_year": 2020,
            "total_caught": 6,
            "standing": "G",
            "year": 2,
            "last_seen_time": "2022-12-11 00:54:34",
            "caught": 0
        },
    "123456":
        {
            "name": "Dilshan Gamage",
            "offence": "ML Engineer",
            "firstcase_year": 2021,
            "total_caught": 6,
            "standing": "G",
            "year": 3,
            "last_seen_time": "2022-12-11 00:54:34",
            "caught": 0
        },
    "123654":
        {
            "name": "Sewwandi Kurera",
            "offence": "Mechatronics",
            "firstcase_year": 2021,
            "total_caught": 6,
            "standing": "G",
            "year": 3,
            "last_seen_time": "2022-12-11 00:54:34",
            "caught": 0
        }
}

for key,value in data.items():
    ref.child(key).set(value)