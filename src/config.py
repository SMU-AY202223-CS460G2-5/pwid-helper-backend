import os

from dotenv import load_dotenv

load_dotenv()


def load_config(config_name: str) -> str:
    config = os.getenv(config_name)
    if not config:
        raise Exception(f"{config_name} is not set")
    return config


TELEGRAM_BOT_TOKEN = load_config("TELEGRAM_BOT_TOKEN")
