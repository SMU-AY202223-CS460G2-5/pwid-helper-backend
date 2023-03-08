from typing import Union

import requests

from src.config import TELEGRAM_BOT_TOKEN
from src.rest import Json, generate_response_json


class TelegramApiWrapper:
    def __init__(self, token: str) -> None:
        self.token = token

    def _post_json(self, json: Json, url: str) -> Json:
        r = requests.post(url, json)
        print(f"{r.status_code}:: {url} :: {json}")
        return r.json()

    def get_url(self, method: str) -> str:
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def get_me(self) -> Json:
        return self._post_json({}, self.get_url("getMe"))

    # Sends a message represented in JSON
    def send_message(self, json: Json) -> Json:
        return self._post_json(json, self.get_url("sendMessage"))

    def send_chat_action(self, json: Json) -> Json:
        return self._post_json(json, self.get_url("sendChatAction"))

    def delete_message(self, json: Json) -> Json:
        return self._post_json(json, self.get_url("deleteMessage"))

    def answer_callback_query(self, json: Json) -> Json:
        return self._post_json(json, self.get_url("answerCallbackQuery"))

    def edit_message_text(self, json: Json) -> Json:
        return self._post_json(json, self.get_url("editMessageText"))

    def edit_message_reply_markup(self, json: Json) -> Json:
        return self._post_json(json, self.get_url("editMessageReplyMarkup"))

    def set_webhook(self, webhookUrl: str) -> Json:
        return self._post_json({"url": webhookUrl}, self.get_url("setWebhook"))

    def clear_webhook(self) -> Json:
        return self.set_webhook("")


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
            chat_id=str(chat_id),
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

    def set_webhook(self, webhookUrl: str) -> Json:
        return self.api.set_webhook(webhookUrl)

    def clear_webhook(self) -> Json:
        return self.api.clear_webhook()

    def get_me(self) -> Json:
        return self.api.get_me()


bot = TelegramBot(TELEGRAM_BOT_TOKEN)
