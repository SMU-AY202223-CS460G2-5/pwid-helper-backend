class MockRequests:
    START_COMMAND = {
        "update_id": 123,
        "message": {
            "message_id": 1,
            "from": {
                "id": 123,
                "is_bot": False,
                "first_name": "FirstName",
                "username": "someusername",
                "language_code": "en",
            },
            "chat": {
                "id": 123,
                "first_name": "FirstName",
                "username": "someusername",
                "type": "private",
            },
            "date": 1678107080,
            "text": "/start",
            "entities": [{"offset": 0, "length": 6, "type": "bot_command"}],
        },
    }


class MockResponse:
    HEALTH = b"Hello, Health!"
    START_COMMAND = {
        "data": {"chat_id": 123, "message_id": 2, "available": True},
        "success": True,
    }
