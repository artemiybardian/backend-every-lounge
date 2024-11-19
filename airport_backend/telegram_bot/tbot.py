import telebot
from telebot.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
)
import requests
import logging
from datetime import datetime, timedelta
# import threading

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_TOKEN = '7702184372:AAFpYNtn0V1MJRYB7BwgYVkd1pBhdWvSXCU'
DJANGO_API_URL = 'https://lounge-booking.com/api/users/auth/'
WEBAPP_URL = 'https://lounge-booking.com/'

# Хранилище кнопок
buttons_store = {}

bot = telebot.TeleBot(API_TOKEN)


# # Фоновая задача для удаления устаревших кнопок
# def cleanup_old_buttons():
#     while True:
#         now = datetime.now()
#         to_update = []

#         for key, value in buttons_store.items():
#             if now - value['timestamp'] > timedelta(days=1):
#                 try:
#                     # Обновляем сообщение с текстом "Обновите местоположение"
#                     bot.edit_message_text(
#                         chat_id=value['chat_id'],
#                         message_id=value['message_id'],
#                         text="⏳ Пожалуйста, обновите ваше местоположение!",
#                         reply_markup=create_location_button()
#                     )
#                     to_update.append(key)
#                 except Exception as e:
#                     logger.error(f"Ошибка обновления сообщения: {e}")

#         # Удаляем записи из хранилища
#         for key in to_update:
#             del buttons_store[key]

#         # Проверяем каждые 10 минут
#         threading.Event().wait(600)


# def create_location_button():
#     """
#     Создает клавиатуру с кнопкой "Отправить местоположение".
#     """
#     keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
#     location_button = KeyboardButton(
#         text="Отправить местоположение", request_location=True)
#     keyboard.add(location_button)
#     return keyboard


# # Запускаем фоновую задачу
# threading.Thread(target=cleanup_old_buttons, daemon=True).start()


# Обработка команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    logger.info("Команда /start получена от %s", message.from_user.username)

    # Приветственное сообщение
    welcome_text = (
        "✈️ **Добро пожаловать в Every Lounge WebApp!**\n\n"
        "Забронируйте доступ в лучшие залы ожидания аэропортов по всему миру. "
        "Просто следуйте инструкциям, и мы подберем для вас ближайший доступный зал.\n\n"
        "Нам нужна ваша локация для подбора лучших залов."
        "Нажмите **'Отправить локацию'**, чтобы продолжить!"
    )

    # Кнопка "Отправить локацию"
    # Можете указать row_width для того, чтобы кнопки выстраивались в одну колонку
    keyboard = InlineKeyboardMarkup(row_width=1)
    start_button = InlineKeyboardButton(
        text="Отправить своё местоположение", request_location=True)
    keyboard.add(start_button)

    bot.send_message(message.chat.id, welcome_text,
                     reply_markup=keyboard, parse_mode='Markdown')

    bot.send_message(
        message.chat.id, welcome_text, reply_markup=keyboard, parse_mode='Markdown')



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
                    text="Перейти в приложение😊",
                    web_app=WebAppInfo(f"{WEBAPP_URL}?token={access_token}")
                )
                keyboard.add(button)

                # Отправляем сообщение с кнопкой
                sent_message = bot.send_message(
                    message.chat.id,
                    "Переходите в приложение по кнопке ниже:",
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
