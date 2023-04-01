import json
from enum import Enum, StrEnum
from time import time
from typing import Any, Generator

from google.cloud.firestore import DocumentSnapshot

from src.constants import Message
from src.firebase import db
from src.rest import Json
from src.telegram import bot, inline_button_with_callback

ALL_USER_STREAM = db.collection("users").stream()
AVAILABLE_USER_STREAM = db.collection("users").where("available", "==", True).stream()


class OnboardingState(Enum):
    NEW = 1
    STARTED = 2
    HAVE_GENDER = 3
    HAVE_LANGUAGE = 4
    COMPLETED = 5


class GenderPreference(StrEnum):
    MALE = "M"
    FEMALE = "F"


class LanguagePreference(StrEnum):
    ENGLISH = "en"
    CHINESE = "cn"
    HOKKIEN = "hk"

    @staticmethod
    def to_list_str() -> list[str]:
        return [lang.name.title() for lang in LanguagePreference]


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


def request_volunteer_gender(user_id: str) -> Json:
    """Ask volunteer for their gender

    Args:
        user_id (str): volunteer's user id
    """
    ask_gender_msg = Message.GENDER_REQUEST
    inline_keyboard_row_0_buttons = [
        inline_button_with_callback(
            text=GenderPreference.MALE.name.title(),
            callback_command="gender",
            callback_value=GenderPreference.MALE.value,
        ),
        inline_button_with_callback(
            text=GenderPreference.FEMALE.name.title(),
            callback_command="gender",
            callback_value=GenderPreference.FEMALE.value,
        ),
    ]
    inline_buttons_markup = [inline_keyboard_row_0_buttons]
    return bot.send_message(
        chat_id=user_id,
        msg=ask_gender_msg,
        markup=dict(inline_keyboard=inline_buttons_markup),
    )


def request_volunteer_language(user_id: str) -> Json:
    """Ask volunteer for their prefered language

    Args:
        user_id (str): volunteer's user id
    """
    ask_language_poll_qn = Message.LANGUAGE_POLL_QUESTION
    language_options = LanguagePreference.to_list_str()
    return bot.send_poll(
        chat_id=user_id,
        question=ask_language_poll_qn,
        options=language_options,
        allows_multiple_answers=True,
    )


def get_user_onboarding_state(username: str) -> OnboardingState:
    """Get user onboarding state

    Args:
        username (str): user's username

    Returns:
        OnboardingState: onboarding state
    """
    doc_ref = db.collection("users").document(username)
    doc_data = doc_ref.get().to_dict() or {}
    return OnboardingState(doc_data.get("onboarding_state", OnboardingState.NEW.value))
