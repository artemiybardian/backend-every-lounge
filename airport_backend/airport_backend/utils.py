import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_telegram_notification(user_telegram_id, message):
    token = '7702184372:AAFpYNtn0V1MJRYB7BwgYVkd1pBhdWvSXCU'
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": user_telegram_id,
        "text": message
    }
    response = requests.post(url, data=data)
    logging.info(f"Telegram response: {response.json()}")
