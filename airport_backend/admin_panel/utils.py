from .models import AdminActionLog
import requests
import logging 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def log_admin_action(admin_user, action_description):
    AdminActionLog.objects.create(
        admin_user=admin_user, action=action_description)


def send_telegram_notification(user_telegram_id, message):
    token = '7702184372:AAFpYNtn0V1MJRYB7BwgYVkd1pBhdWvSXCU'
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": user_telegram_id,
        "text": message
    }
    response = requests.post(url, data=data)

    # Логируем ответ для отладки
    logger.info(f"Telegram response: {response.json()}")

    if response.status_code != 200:
        logger.error(f"Ошибка отправки сообщения: {response.json()}")
