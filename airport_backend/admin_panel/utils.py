from .models import AdminActionLog
import requests
import logging 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def log_admin_action(admin_user, action_description):
    AdminActionLog.objects.create(
        admin_user=admin_user, action=action_description)


def send_telegram_notification(user_telegram_id, message):
    try:
        # Убедитесь, что это целое число
        user_telegram_id = int(user_telegram_id)
    except ValueError:
        logging.error(
            "Некорректный формат user_telegram_id: не является числом")
        return

    token = '7702184372:AAFpYNtn0V1MJRYB7BwgYVkd1pBhdWvSXCU'
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": user_telegram_id,
        "text": message
    }
    response = requests.post(url, data=data)
    logging.info(f"Telegram response: {response.json()}")
