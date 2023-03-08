import requests

from src.config import TELEGRAM_BOT_TOKEN
from src.rest import Json, generate_response_json


class TelegramApiWrapper:
    def __init__(self, token):
        self.token = token

    def _post_json(self, json: Json, url):
        r = requests.post(url, json)
        print(f"{r.status_code}:: {url} :: {json}")
        return r.json()

    def get_url(self, method):
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def get_me(self):
        return self._post_json({}, self.get_url("getMe"))

    # Sends a message represented in JSON
    def send_message(self, json: Json):
        return self._post_json(json, self.get_url("sendMessage"))

    def send_chat_action(self, json: Json):
        return self._post_json(json, self.get_url("sendChatAction"))

    def delete_message(self, json: Json):
        return self._post_json(json, self.get_url("deleteMessage"))

    def answer_callback_query(self, json: Json):
        return self._post_json(json, self.get_url("answerCallbackQuery"))

    def edit_message_text(self, json: Json):
        return self._post_json(json, self.get_url("editMessageText"))

    def edit_message_reply_markup(self, json: Json):
        return self._post_json(json, self.get_url("editMessageReplyMarkup"))

    def set_webhook(self, webhookUrl):
        return self._post_json({"url": webhookUrl}, self.get_url("setWebhook"))

    def clear_webhook(self):
        return self.set_webhook("")


class TelegramBot:
    def __init__(self, token):
        self.api = TelegramApiWrapper(token)

    def send_message(self, chat_id: int, msg: str, markup=None):
        """Sends a message to a telegram chat.

        Refer to Telegram API for necessary parameters.
        https://core.telegram.org/bots/api#sendmessage

        Args:
            chat_id (int): The chat id of the chat to send this message to.
            msg (str): The message to be sent.
            markup (str, optional): The reply markup type of the message. Defaults
                to None.

        Returns:
            SentUpdateResponse: a json payload for response containing response from
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
            resp_result = resp.get("result")
            resp_chat_id = resp_result.get("chat").get("id")
            resp_message_id = resp_result.get("message_id")
            data = {"chat_id": resp_chat_id, "message_id": resp_message_id}
        else:
            data = dict(error=resp.get("description"))

        return generate_response_json(success, data)

    def send_chat_action(self, chat_id, action):
        json = {
            "chat_id": chat_id,
            "action": action,
        }
        return self.api.send_chat_action(json)

    def delete_message(self, chat_id, message_id):
        json = {
            "chat_id": chat_id,
            "message_id": message_id,
        }
        return self.api.delete_message(json)

    def answer_callback_query(self, callback_query_id, text=None, show_alert=False):
        json = {
            "callback_query_id": callback_query_id,
            "show_alert": show_alert,
        }
        if text:
            json["text"] = text
        return self.api.answer_callback_query(json)

    def edit_message_text(self, chat_id, message_id, text, parse_mode=None):
        json = {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text,
        }
        if parse_mode:
            json["parse_mode"] = parse_mode
        return self.api.edit_message_text(json)

    def edit_message_reply_markup(self, chat_id, message_id, reply_markup):
        json = {
            "chat_id": chat_id,
            "message_id": message_id,
            "reply_markup": reply_markup,
        }
        return self.api.edit_message_reply_markup(json)

    def set_webhook(self, webhookUrl):
        return self.api.set_webhook(webhookUrl)

    def clear_webhook(self):
        return self.api.clear_webhook()

    def get_me(self):
        return self.api.get_me()


bot = TelegramBot(TELEGRAM_BOT_TOKEN)
