import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from pathlib import Path

# Use a service account
cred = credentials.Certificate(
    Path(__file__).parent.joinpath(
        "fleshid-dc8ed-firebase-adminsdk-cvknm-51a90eaf75.json"
    )
)

firebase_admin.initialize_app(cred)

# Access Firestore using the default project ID
db = firestore.client()
