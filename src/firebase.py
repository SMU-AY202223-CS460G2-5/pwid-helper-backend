from pathlib import Path
from typing import Any, Dict

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore import Client

cred = credentials.Certificate(
    Path(__file__).parent.joinpath(
        "fleshid-dc8ed-firebase-adminsdk-cvknm-51a90eaf75.json"
    )
)

firebase_admin.initialize_app(cred)
db: Client = firestore.client()


def available() -> Dict[str, Any]:
    collection_ref = db.collection("users")
    docs = collection_ref.get()
    result = {d.get("username"): d.to_dict() for d in docs if d.get("available")}
    return result


def change_available(username: str) -> None:
    doc_ref = db.collection("users").document(username)
    doc_data = doc_ref.get().to_dict()

    my_field = doc_data["available"]
    if my_field:
        doc_ref.update({"available": False})
    else:
        doc_ref.update({"available": True})
