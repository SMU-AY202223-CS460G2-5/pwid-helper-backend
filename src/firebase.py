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

def available():
    result = {}
    collection_ref = db.collection('users')
    docs = collection_ref.get()

    for doc in docs:
        if doc.get("available"):
            result[doc.get("username")] = doc.to_dict()


    return(result)

def change_available(username):
    doc_ref = db.collection('users').document(username)
    doc_data = doc_ref.get().to_dict()

    my_field = doc_data["available"]
    if my_field:
        doc_ref.update({'available': False})
    else:
        doc_ref.update({'available': True})
