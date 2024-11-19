import telebot
from telebot.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton,
    WebAppInfo
)
import requests
import logging
from datetime import datetime

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_TOKEN = '7702184372:AAFpYNtn0V1MJRYB7BwgYVkd1pBhdWvSXCU'
DJANGO_API_URL = 'https://lounge-booking.com/api/users/auth/'
WEBAPP_URL = 'https://lounge-booking.com/'

bot = telebot.TeleBot(API_TOKEN)

# Обработка команды /start


@bot.message_handler(commands=['start'])
def send_welcome(message):
    logger.info("Команда /start получена от %s", message.from_user.username)

    # Приветственное сообщение
    welcome_text = (
        "✈️ **Добро пожаловать в Every Lounge WebApp!**\n\n"
        "Забронируйте доступ в лучшие залы ожидания аэропортов по всему миру. "
        "Просто следуйте инструкциям, и мы подберем для вас ближайший доступный зал.\n\n"
        "📍 Пожалуйста, отправьте ваше местоположение, чтобы мы нашли ближайшие залы ожидания!\n\n"
        "Нажмите **'Отправить местоположение'**, чтобы продолжить!"
    )

    # Кнопка "Начать бронирование"
    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    location_button = KeyboardButton(
        text="Отправить местоположение", request_location=True)
    keyboard.add(location_button)

    bot.send_message(message.chat.id, welcome_text,
                     reply_markup=keyboard, parse_mode='Markdown')


# Обработка кнопки "Начать бронирование"
# @bot.callback_query_handler(func=lambda callback: True)
# def callback_booking(callback):
#     # logger.info("Пользователь %s начал бронирование.", callback.from_user.username)

#     # Запрос местоположения
#     location_request_text = (
#         "📍 Пожалуйста, отправьте ваше местоположение, чтобы мы нашли ближайшие залы ожидания!"
#     )

#     # Кнопка "Отправить местоположение"
#     keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
#     location_button = KeyboardButton(
#         text="Отправить местоположение", request_location=True)
#     keyboard.add(location_button)

#     bot.send_message(callback.message.chat.id, location_request_text,
#                      reply_markup=keyboard)


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
            # Получаем токен доступа из Django API
            response_data = response.json()
            if 'token' in response_data:
                access_token = response_data['token']

                # Создаем кнопку для перехода в WebApp с передачей токена
                keyboard = InlineKeyboardMarkup()
                button = InlineKeyboardButton(
                    text="Забронировать зал😊",
                    web_app=WebAppInfo(f"{WEBAPP_URL}?token={access_token}")
                )
                keyboard.add(button)

                # Отправляем сообщение с кнопкой
                sent_message = bot.send_message(
                    message.chat.id,
                    "Бронируйте залы ожидания аэропортов по кнопке ниже:",
                    reply_markup=keyboard
                )

            else:
                bot.send_message(
                    message.chat.id, "Не удалось получить токен. Попробуйте еще раз.")
        else:
            bot.send_message(message.chat.id, "Ошибка при обновлении данных.")


# Запуск бота
if __name__ == '__main__':
    logger.info("Запуск бота...")
    bot.infinity_polling()
