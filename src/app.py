import logging
import os
from typing import Any, Tuple

from flask import Flask, jsonify, request

from src.constants import Message
from src.firebase import available
from src.telegram import bot
from src.telegram.handlers import (
    MessageCommandTypes,
    callback_query_handler,
    message_handler,
)
from src.telegram.update import TelegramBotUpdate, TelegramBotUpdateTypes

app = Flask(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(levelname)-8s :: (%(name)s) %(message)s"
)
logger = logging.getLogger(__name__)


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
    body = request.get_json() if request.is_json else None
    logger.info(f"request body: {body}")
    if not body:
        return "Invalid Request Body", 400

    update = TelegramBotUpdate(body)
    response = None
    if update.type == TelegramBotUpdateTypes.MESSAGE:
        if update.text == MessageCommandTypes.START:
            response = message_handler.start(update)

    elif update.type == TelegramBotUpdateTypes.CALLBACK_QUERY:
        if update.callback_data.get("command") == "gender":
            response = callback_query_handler.gender_preference(update)
        elif update.callback_data.get("command") == "language":
            response = callback_query_handler.language_preference(update)
    else:
        logger.info(f"Unhandled Update Type: {update.type}")
        response = bot.send_message(update.chat_id, "Invalid input, please try again.")

    if not response:
        return "No response", 200

    logger.info(repr(response))
    return response, 200


@app.route("/setWebhook", methods=["GET"])
def set_webhook() -> Tuple[Any, int]:
    webhook_url = f"https://{request.host}/webhook"
    env = os.getenv("FLASK_ENV")
    if env == "production":
        bot.set_webhook(webhook_url)
    return (
        jsonify(
            webhook_url=webhook_url,
            environment=env,
        ),
        200,
    )


@app.route("/health")
def health() -> Tuple[Any, int]:
    which = request.args.get("which")
    if which == "telegram":
        return bot.get_me(), 200

    return "Hello, Health!", 200


@app.route("/rasp", methods=["POST"])
def rasp() -> Tuple[Any, int]:
    body = request.get_json() if request.is_json else None
    logger.info(f"request body: {body}")

    if not body:
        return "Invalid Request Body", 400

    pwid_id = body.get("id")
    long = body.get("long")
    lat = body.get("lat")

    if not pwid_id or not long or not lat:
        return "Invalid Request Body", 400

    broadcast_message = Message.BROADCAST_REQUEST.format(
        f"Long: {long}, Lat {lat}", pwid_id
    )
    available_volunteers = [
        volunteer.get("chat_id") for volunteer in available().values()
    ]
    bot.broadcast(broadcast_message, available_volunteers)
    logger.info(f"id: {pwid_id}, long: {long}, lat: {lat}")
    return "DUCK", 200
