from .models import AdminActionLog
import requests


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
    requests.post(url, data=data)
