from time import time
from typing import Any, Generator

from google.cloud.firestore import DocumentSnapshot

from src.firebase import db
from src.telegram import bot

ALL_USER_STREAM = db.collection("users").stream()
AVAILABLE_USER_STREAM = db.collection("users").where("available", "==", True).stream()


def broadcast_message_to_stream(
    user_stream: Generator[DocumentSnapshot, Any, None],
    message: str,
) -> None:
    """Broadcast message to all users in stream

    Args:
        user_stream (Generator[DocumentSnapshot, Any, None]): stream of users
        message (str): message to broadcast
    """
    users = [user.id for user in user_stream]
    bot.broadcast(message, users)


def select_security_image() -> str:
    """Select the security image

    Example doc (id = `value`):
        {
            "available": True,
            "updated_at": 1679475161,
            "value": "SMILE"
        }

    Returns:
        str: name of security image
    """
    icon_coll = db.collection("icon_names")
    available_icons = (
        icon_coll.where("available", "==", True)
        .order_by("updated_at", direction="ASCENDING")
        .stream()
    )
    icon = next(available_icons, None)
    if not icon:
        oldest = next(
            icon_coll.order_by("updated_at", direction="ASCENDING").stream(), None
        )
        if not oldest:
            return "SMILE"
        oldest.reference.update(
            dict(
                updated_at=int(time()),
            )
        )
        return oldest.get("value")

    icon.reference.update(
        dict(
            available=False,
            updated_at=int(time()),
        )
    )
    return icon.get("value")
