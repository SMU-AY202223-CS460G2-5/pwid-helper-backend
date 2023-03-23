from src.constants import Message
from src.firebase import db
from src.rest import Json
from src.telegram import TelegramBot, bot
from src.telegram.update import TelegramBotUpdate


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
                available=True,
            )
        )
        return self.bot.send_message(
            update.chat_id,
            Message.START_BOT.format(first_name),
        )


class CallbackQueryHandler:
    def __init__(self, bot: TelegramBot):
        self.bot = bot


message_handler = MessageHandler(bot)
callback_query_handler = CallbackQueryHandler(bot)
