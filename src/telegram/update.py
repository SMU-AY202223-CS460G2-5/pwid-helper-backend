import json
from typing import Any, Dict, Union

from src.rest import Json


class TelegramBotUpdate:
    def __init__(self, update: Dict[str, Any]):
        """Represents a Telegram Bot Update.

        Refer to Telegram API for more details.
        https://core.telegram.org/bots/api#update

        An update can be one of the following:
        - Message
        - Edited Message
        - Channel Post
        - Edited Channel Post
        - Inline Query
        - Chosen Inline Result
        - Callback Query
        - Shipping Query
        - Pre Checkout Query
        - Poll
        - Poll Answer

        Example Update:
        {
            "update_id": 287379129,
            "message": {
                "message_id": 4,
                "from": {
                    "id": 213517771,
                    "is_bot": false,
                    "first_name": "Some User",
                    "username": "someUsername",
                    "language_code": "en"
                },
                "chat": {
                    "id": 213517771,
                    "first_name": "Some User",
                    "username": "someUsername",
                    "type": "private"
                },
                "date": 1678108310,
                "text": "/start"
            }
        }

        Args:
            update (Dict[str, Any]): Telegram Bot Update.
        """
        self.message: Union[Dict[str, Any], None] = update.get("message")
        self.callback_query = update.get("callback_query")
        self.type = None

        if self.message:
            self.type = TelegramBotUpdateTypes.MESSAGE
            self.chat: Dict[str, Any] = self.message.get("chat")
            self.chat_id = int(self.chat.get("id"))  # type: ignore
            self.username: str = self.chat.get("username")  # type: ignore
            self.first_name: str = self.chat.get("first_name")  # type: ignore
            self.message_id = int(self.message.get("message_id"))
            self.text: str = self.message.get("text")

        elif self.callback_query:
            self.type = TelegramBotUpdateTypes.CALLBACK_QUERY
            self.chat: Dict[str, Any] = (  # type: ignore
                # format: off
                self.callback_query.get("message").get("chat")
                # format: on
            )
            self.chat_id = int(self.chat.get("id"))  # type: ignore
            self.username: str = self.chat.get("username")  # type: ignore
            self.first_name: str = self.chat.get("first_name")  # type: ignore
            self.message_id = int(self.callback_query.get("message").get("message_id"))
            self.callback_data: Json = self.callback_query.get("data")  # type: ignore


class TelegramBotUpdateTypes:
    MESSAGE = "message"
    EDITED_MESSAGE = "edited_message"
    CHANNEL_POST = "channel_post"
    EDITED_CHANNEL_POST = "edited_channel_post"
    INLINE_QUERY = "inline_query"
    CHOSEN_INLINE_RESULT = "chosen_inline_result"
    CALLBACK_QUERY = "callback_query"
    SHIPPING_QUERY = "shipping_query"
    PRE_CHECKOUT_QUERY = "pre_checkout_query"
    POLL = "poll"
    POLL_ANSWER = "poll_answer"
