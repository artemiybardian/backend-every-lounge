import telebot
from telebot.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo)
import requests
import logging
from datetime import datetime, timedelta
import threading

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_TOKEN = '7702184372:AAFpYNtn0V1MJRYB7BwgYVkd1pBhdWvSXCU'
DJANGO_API_URL = 'https://lounge-booking.com/api/users/auth/'
WEBAPP_URL = 'https://lounge-booking.com/'

# Хранилище кнопок
buttons_store = {}

bot = telebot.TeleBot(API_TOKEN)

# Фоновая задача для удаления устаревших кнопок


def cleanup_old_buttons():
    while True:
        now = datetime.now()
        to_delete = []

        for key, value in buttons_store.items():
            if now - value['timestamp'] > timedelta(days=1):
                try:
                    # Удаление кнопки из сообщения
                    bot.edit_message_reply_markup(
                        chat_id=value['chat_id'], message_id=value['message_id'], reply_markup=None)
                    to_delete.append(key)
                except Exception as e:
                    logger.error(f"Ошибка удаления кнопки: {e}")

        # Удаление из хранилища
        for key in to_delete:
            del buttons_store[key]

        # Проверяем каждые 10 минут
        threading.Event().wait(600)


# Запускаем фоновую задачу
threading.Thread(target=cleanup_old_buttons, daemon=True).start()

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
            },
        }

        # Отправляем данные на Django API
        response = requests.post(DJANGO_API_URL, json=data)
        logger.info("Отправлены данные на Django: %s", data)

        if response.status_code == 200:
            bot.send_message(message.chat.id, "Ваши данные успешно обновлены.")

            # Получаем токен доступа из Django API
            response_data = response.json()
            if 'token' in response_data:
                access_token = response_data['token']

                # Создаем кнопку для перехода в WebApp с передачей токена
                keyboard = InlineKeyboardMarkup()
                button = InlineKeyboardButton(
                    text="Перейти в WebApp",
                    web_app=WebAppInfo(f"{WEBAPP_URL}?token={access_token}")
                )
                keyboard.add(button)

                # Отправляем сообщение с кнопкой
                sent_message = bot.send_message(
                    message.chat.id,
                    "Вы можете перейти в ваш аккаунт в WebApp, нажав на кнопку ниже:",
                    reply_markup=keyboard
                )

                # Сохраняем информацию о кнопке
                buttons_store[sent_message.message_id] = {
                    'chat_id': sent_message.chat.id,
                    'message_id': sent_message.message_id,
                    'timestamp': datetime.now()
                }
            else:
                bot.send_message(
                    message.chat.id, "Не удалось получить токен. Попробуйте еще раз.")
        else:
            bot.send_message(message.chat.id, "Ошибка при обновлении данных.")


# Запуск бота
if __name__ == '__main__':
    logger.info("Запуск бота...")
    bot.infinity_polling()
