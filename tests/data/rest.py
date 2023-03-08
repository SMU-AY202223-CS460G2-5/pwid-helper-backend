class MockRequests:
    START_COMMAND = {
        "update_id": 287379127,
        "message": {
            "message_id": 1,
            "from": {
                "id": 238013249,
                "is_bot": False,
                "first_name": "David",
                "username": "davidlhw",
                "language_code": "en",
            },
            "chat": {
                "id": 238013249,
                "first_name": "David",
                "username": "davidlhw",
                "type": "private",
            },
            "date": 1678107080,
            "text": "/start",
            "entities": [{"offset": 0, "length": 6, "type": "bot_command"}],
        },
    }
    pass


class MockResponse:
    HEALTH = b"Hello, Health!"
