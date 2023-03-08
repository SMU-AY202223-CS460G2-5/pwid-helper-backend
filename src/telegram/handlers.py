from src.constants import Message
from src.rest import Json
from src.telegram import TelegramBot, bot
from src.telegram.update import TelegramBotUpdate


class MessageCommandTypes:
    START = "/start"


class MessageHandler:
    def __init__(self, bot: TelegramBot):
        self.bot = bot

    def start(self, update: TelegramBotUpdate) -> Json:
        return self.bot.send_message(
            update.chat_id,
            Message.START_BOT,
        )


class CallbackQueryHandler:
    def __init__(self, bot: TelegramBot):
        self.bot = bot


message_handler = MessageHandler(bot)
callback_query_handler = CallbackQueryHandler(bot)
