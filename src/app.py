from typing import Any, Tuple

from flask import Flask, request

from src.rest import Json
from src.telegram import bot
from src.telegram.handlers import MessageCommandTypes, message_handler
from src.telegram.update import TelegramBotUpdate, TelegramBotUpdateTypes
from src.firebase import available, change_available

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook() -> Tuple[Any, int]:
    """Telegram Bot Webhook Endpoint

    Example Request Body:
        {
            "update_id": 123456789,
            "message": {
                "message_id": 123,
                "from": {
                    "id": 123456789,
                    "is_bot": false,
                    "first_name": "John",
                    "last_name": "Doe",
                    "username": "johndoe",
                    "language_code": "en"
                },
                "chat": {
                    "id": 123456789,
                    "first_name": "John",
                    "last_name": "Doe",
                    "username": "johndoe",
                    "type": "private"
                },
                "date": 1620000000,
                "text": "/start",
                "entities": [{ "offset": 0, "length": 6, "type": "bot_command" }]
            }
        }

    Returns:
        Tuple[Any, int]: Flask Response
    """
    available()
    body = request.get_json() if request.is_json else None
    if not body:
        return "Invalid Request Body", 400

    update = TelegramBotUpdate(body)
    response = None
    if update.type == TelegramBotUpdateTypes.MESSAGE:
        if update.text == MessageCommandTypes.START:
            response = message_handler.start(update)


    if not response:
        return "Telegram Api Error", 500

    return response, 200


@app.route("/setWebhook", methods=["GET"])
def set_webhook() -> Tuple[Any, int]:
    bot.set_webhook(request.url_root + "webhook")
    return request.url_root, 200


@app.route("/health", methods=["GET"])
def health() -> Tuple[Any, int]:
    which = request.args.get("which")
    if which == "telegram":
        return bot.get_me(), 200

    return "Hello, Health!", 200


@app.route("/rasp", methods=["POST"])
def rasp() -> Tuple[Any, int]:
    return "Hello, Raspberry Pi!", 200
