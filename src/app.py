from flask import Flask, request

from src.rest import Json
from src.telegram import bot
from src.telegram.handlers import MessageCommandTypes, message_handler
from src.telegram.update import TelegramBotUpdate, TelegramBotUpdateTypes

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():
    """Telegram Bot Webhook Endpoint



    Returns:
        _type_: _description_
    """
    body = None
    if request.is_json:
        body: Json = request.get_json()
    if not body:
        return "Invalid Request Body", 400

    update = TelegramBotUpdate(body)
    response = None
    if update.type == TelegramBotUpdateTypes.MESSAGE:
        if update.text == MessageCommandTypes.START:
            response = message_handler.start(update)

    if not response:
        return "Telegram Api Error", 500

    return response


@app.route("/setWebhook", methods=["GET"])
def set_webhook():
    bot.set_webhook(request.url_root + "webhook")
    return request.url_root


@app.route("/health", methods=["GET"])
def health():
    return "Hello, Health!"


@app.route("/rasp", methods=["POST"])
def rasp():
    return "Hello, Raspberry Pi!"
