from time import time

from src.constants import Message
from src.firebase import db
from src.rest import Json
from src.telegram import TelegramBot, bot
from src.telegram.update import TelegramBotUpdate
from src.telegram.volunteers import (
    GenderPreference,
    LanguagePreference,
    OnboardingState,
    request_volunteer_gender,
    request_volunteer_language,
)


class MessageCommandTypes:
    START = "/start"


class MessageHandler:
    def __init__(self, bot: TelegramBot):
        self.bot = bot

    def start(self, update: TelegramBotUpdate) -> Json:
        username = update.username
        doc_ref = db.collection("users").document(username)
        doc = doc_ref.get()
        if doc.exists:
            return self.bot.send_message(
                update.chat_id,
                Message.START_BOT_USER_ALREADY_EXIST,
            )
        first_name = update.first_name
        chat_id = update.chat_id
        doc_ref.set(
            dict(
                username=username,
                first_name=first_name,
                chat_id=chat_id,
                available=False,
                onboarding_state=OnboardingState.NEW.value,
                created_at=int(time()),
                updated_at=int(time()),
            )
        )
        return request_volunteer_gender(chat_id)


class CallbackQueryHandler:
    def __init__(self, bot: TelegramBot):
        self.bot = bot

    def gender_preference(self, update: TelegramBotUpdate) -> Json:
        callback_data = update.callback_data
        username = update.username
        doc_ref = db.collection("users").document(username)
        doc_ref.update(
            dict(
                gender=GenderPreference(callback_data.get("value")).value,
                updated_at=int(time()),
            )
        )
        bot.answer_callback_query(update.callback_query_id)
        return request_volunteer_language(update.chat_id)

    def language_preference(self, update: TelegramBotUpdate) -> Json:
        callback_data = update.callback_data
        username = update.username
        doc_ref = db.collection("users").document(username)
        doc_ref.update(
            dict(
                available=True,
                language=LanguagePreference(callback_data.get("value")).value,
                updated_at=int(time()),
            )
        )
        bot.answer_callback_query(update.callback_query_id)
        return self.bot.send_message(
            update.chat_id,
            Message.ONBOARD_SUCCESS.format(username),
        )

    def accept_volunteer(self, update: TelegramBotUpdate) -> Json:
        callback_data = update.callback_data
        username = update.username
        doc_ref = db.collection("users").document(username)
        doc_ref.update(
            dict(
                available=False,
                updated_at=int(time()),
            )
        )
        bot.answer_callback_query(update.callback_query_id)
        self.bot.send_message(
            update.chat_id,
            Message.ACCEPTED_REQUEST,
        )
        return self.bot.send_photo(
            update.chat_id,
            photo_url="https://firebasestorage.googleapis.com/v0/b/fleshid-dc8ed.appspot.com/o/microbit-duck.png?alt=media",
        )


message_handler = MessageHandler(bot)
callback_query_handler = CallbackQueryHandler(bot)
