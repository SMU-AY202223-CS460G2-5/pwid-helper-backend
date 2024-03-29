import json
import logging
from typing import List, Union

import requests

from src.config import TELEGRAM_BOT_TOKEN
from src.rest import Json, generate_response_json

logger = logging.getLogger(__name__)


class TelegramApiWrapper:
    def __init__(self, token: str) -> None:
        self.token = token

    def _post_json(self, json: Json, url: str) -> Json:
        """Sends a POST request to the Telegram API."""
        r = requests.post(url, json=json)
        print(f"{url} :: {json}")
        logger.info(f"{url} :: {json}")
        logger.info(f"{r.status_code} :: {r.json()}")
        return r.json()

    def get_url(self, method: str) -> str:
        """Returns the Telegram API URL for a given method."""
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def get_me(self) -> Json:
        """Returns basic information about the bot in form of a user object.

        Refer to Telegram API for more details.
        https://core.telegram.org/bots/api#getme
        """
        return self._post_json({}, self.get_url("getMe"))

    def send_message(self, json: Json) -> Json:
        """Sends a message to a telegram chat.

        Refer to Telegram API for necessary parameters.
        https://core.telegram.org/bots/api#sendmessage
        """
        return self._post_json(json, self.get_url("sendMessage"))

    def send_poll(self, json: Json) -> Json:
        """Sends a poll to a telegram chat.

        Refer to Telegram API for necessary parameters.
        https://core.telegram.org/bots/api#sendpoll
        """
        return self._post_json(json, self.get_url("sendPoll"))

    def send_chat_action(self, json: Json) -> Json:
        """Sends a chat action to a telegram chat.

        Refer to Telegram API for necessary parameters.
        https://core.telegram.org/bots/api#sendchataction
        """
        return self._post_json(json, self.get_url("sendChatAction"))

    def delete_message(self, json: Json) -> Json:
        """Deletes a message from a telegram chat.

        Refer to Telegram API for necessary parameters.
        https://core.telegram.org/bots/api#deletemessage
        """
        return self._post_json(json, self.get_url("deleteMessage"))

    def answer_callback_query(self, json: Json) -> Json:
        """Answer a callback query.

        Refer to Telegram API for necessary parameters.
        https://core.telegram.org/bots/api#answercallbackquery
        """
        return self._post_json(json, self.get_url("answerCallbackQuery"))

    def edit_message_text(self, json: Json) -> Json:
        """Edit a message text.

        Refer to Telegram API for necessary parameters.
        https://core.telegram.org/bots/api#editmessagetext
        """
        return self._post_json(json, self.get_url("editMessageText"))

    def edit_message_reply_markup(self, json: Json) -> Json:
        """Edit a message reply markup.

        Refer to Telegram API for necessary parameters.
        https://core.telegram.org/bots/api#editmessagereplymarkup
        """
        return self._post_json(json, self.get_url("editMessageReplyMarkup"))

    def set_webhook(self, webhook_url: str) -> Json:
        """Set a webhook url for the bot.

        Refer to Telegram API for necessary parameters.
        https://core.telegram.org/bots/api#setwebhook
        """
        return self._post_json({"url": webhook_url}, self.get_url("setWebhook"))

    def delete_webhook(self) -> Json:
        """Deletes the webhook url for the bot.

        Refer to Telegram API for necessary parameters.
        https://core.telegram.org/bots/api#deletewebhook
        """
        return self._post_json(
            {"drop_pending_updates": True}, self.get_url("deleteWebhook")
        )

    def send_photo(self, chat_id: int, photo_url: str) -> Json:
        """Send a photo to a telegram chat.

        Refer to Telegram API for necessary parameters.
        https://core.telegram.org/bots/api#sendphoto
        """
        return self._post_json(
            {"chat_id": chat_id, "photo": photo_url}, self.get_url("sendPhoto")
        )


class TelegramBot:
    def __init__(self, token: str) -> None:
        self.api = TelegramApiWrapper(token)

    def send_message(
        self,
        chat_id: int,
        msg: str,
        markup: Union[str, None] = None,
    ) -> Json:
        """Sends a message to a telegram chat.

        Refer to Telegram API for necessary parameters.
        https://core.telegram.org/bots/api#sendmessage

        Args:
            chat_id (int): The chat id of the chat to send this message to.
            msg (str): The message to be sent.
            markup (str, optional): The reply markup type of the message. Defaults
                to None.

        Returns:
            Json: a json payload for response containing response from
                telegram api.
        """
        payload = dict(
            chat_id=int(chat_id),
            text=msg,
            parse_mode="HTML",
        )
        if markup:
            payload["reply_markup"] = markup

        resp = self.api.send_message(payload)
        success = resp.get("ok")
        if success:
            try:
                resp_result = resp.get("result")  # type: ignore
                resp_chat_id = resp_result.get("chat").get("id")  # type: ignore
                resp_message_id = resp_result.get("message_id")  # type: ignore
                data = dict(chat_id=resp_chat_id, message_id=resp_message_id)
            except AttributeError:
                data = dict(error="Invalid response from telegram api")
        else:
            data = dict(error=resp.get("description"))

        return generate_response_json(success, data)

    def send_photo(self, chat_id: int, photo_url: str):
        return self.api.send_photo(chat_id, photo_url)

    def send_poll(
        self,
        chat_id: int,
        question: str,
        options: List[str],
        allows_multiple_answers: bool = False,
        open_period: int = 600,
        protect_content: bool = True,
        markup: Union[str, None] = None,
    ) -> Json:
        """Sends a poll to a telegram chat.

        Args:
            chat_id (int): The chat id of the chat to send this message to.
            question (str): The question of the poll.
            options (List[str]): A list of answer options, 2-10 strings 1-100
                characters each.
            allows_multiple_answers (bool, optional): True, if the poll allows
                multiple answers. Defaults to False.
            open_period (int, optional): Amount of time in seconds the poll will
                be active after creation. Defaults to 600.
            protect_content (bool, optional): True, if the poll needs to be sent
                anonymously. Defaults to True.
            markup (str, optional): The reply markup type of the message. Defaults
                to None.

        Returns:
            Json: a json payload for response containing response from telegram api.
        """
        poll = dict(
            chat_id=chat_id,
            question=question,
            options=options,
            is_anonymous=protect_content,
            type="regular",
            allows_multiple_answers=allows_multiple_answers,
            open_period=open_period,
            reply_markup=markup,
        )
        poll = {k: v for k, v in poll.items() if v is not None}
        logger.info(f"Sending poll: {poll}")
        self.api.send_poll(poll)

    def broadcast(self, message: str, chat_ids: List[int], markup=None) -> None:
        """Broadcast Message to list of Users

        Args:
            message (str): message to broadcast
            users (List[str]): list of user's chat id
        """
        for chat_id in chat_ids:
            self.send_message(chat_id, message, markup)

    def send_chat_action(self, chat_id: int, action: str) -> Json:
        json = {
            "chat_id": chat_id,
            "action": action,
        }
        return self.api.send_chat_action(json)

    def delete_message(self, chat_id: int, message_id: int) -> Json:
        json = {
            "chat_id": chat_id,
            "message_id": message_id,
        }
        return self.api.delete_message(json)

    def answer_callback_query(
        self,
        callback_query_id: int,
        text: Union[str, None] = None,
        show_alert: bool = False,
    ) -> Json:
        json = {
            "callback_query_id": callback_query_id,
            "show_alert": show_alert,
        }
        if text:
            json["text"] = text  # type: ignore
        return self.api.answer_callback_query(json)

    def edit_message_text(
        self,
        chat_id: int,
        message_id: int,
        text: str,
        parse_mode: Union[str, None] = None,
    ) -> Json:
        json = {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text,
        }
        if parse_mode:
            json["parse_mode"] = parse_mode
        return self.api.edit_message_text(json)

    def edit_message_reply_markup(
        self,
        chat_id: int,
        message_id: int,
        reply_markup: Union[str, None] = None,
    ) -> Json:
        json = {
            "chat_id": chat_id,
            "message_id": message_id,
            "reply_markup": reply_markup,
        }
        return self.api.edit_message_reply_markup(json)

    def set_webhook(self, webhook_url: str) -> Json:
        return self.api.set_webhook(webhook_url)

    def delete_webhook(self) -> Json:
        return self.api.delete_webhook()

    def get_me(self) -> Json:
        return self.api.get_me()


def inline_button_with_callback(
    text: str, callback_command: str, callback_value: str
) -> Json:
    a = dict(
        text=text,
        callback_data=json.dumps(dict(command=callback_command, value=callback_value)),
    )
    return a


bot = TelegramBot(TELEGRAM_BOT_TOKEN)
