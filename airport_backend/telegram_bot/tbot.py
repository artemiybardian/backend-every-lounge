import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import requests
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_TOKEN = '7702184372:AAFpYNtn0V1MJRYB7BwgYVkd1pBhdWvSXCU'
DJANGO_API_URL = 'http://127.0.0.1:8000/api/users/auth/'

bot = telebot.TeleBot(API_TOKEN)

# Обработка команды /start


@bot.message_handler(commands=['start'])
def send_welcome(message):
    logger.info("Команда /start получена от %s", message.from_user.username)

    # Создаем клавиатуру с кнопкой для отправки местоположения
    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    location_button = KeyboardButton(
        text="Отправить своё местоположение", request_location=True)
    keyboard.add(location_button)

    bot.send_message(
        message.chat.id, "Пожалуйста, отправьте своё текущее местоположение, нажав на кнопку ниже.", reply_markup=keyboard)

# Обработка местоположения пользователя


@bot.message_handler(content_types=['location'])
def handle_location(message):
    if message.location is not None:
        logger.info("Получено местоположение от пользователя %s",
                    message.from_user.username)

        latitude = message.location.latitude
        longitude = message.location.longitude
        telegram_id = message.from_user.id
        username = message.from_user.username
        first_name = message.from_user.first_name if message.from_user.first_name else None
        last_name = message.from_user.last_name if message.from_user.last_name else None

        data = {
            "telegram_id": telegram_id,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "location": {
                "latitude": latitude,
                "longitude": longitude
            }
        }

        # Отправляем данные на Django API
        response = requests.post(DJANGO_API_URL, json=data)
        logger.info("Отправлены данные на Django: %s", data)

        if response.status_code == 200:
            bot.send_message(message.chat.id, "Ваши данные успешно обновлены.")
        else:
            bot.send_message(message.chat.id, "Ошибка при обновлении данных.")


# Запуск бота
if __name__ == '__main__':
    logger.info("Запуск бота...")
    bot.infinity_polling()
