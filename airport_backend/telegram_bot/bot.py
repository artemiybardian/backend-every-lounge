from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
import requests

API_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
DJANGO_API_URL = 'https://127.0.0.1:8000/api/users/auth/'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)



# Обработка команды /start, запрос местоположения и отправка username
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    telegram_id = message.from_user.id
    # Проверка наличия username
    username = message.from_user.username if message.from_user.username else None

    # Запрашиваем у пользователя местоположение
    location_button = KeyboardButton(
        "Отправить своё местоположение", request_location=True)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(location_button)

    # Отправляем telegram_id и username (или None) на сервер
    data = {
        "telegram_id": telegram_id,
        "username": username
    }
    response = requests.post(DJANGO_API_URL, json=data)

    await message.answer("Пожалуйста, отправьте своё текущее местоположение, нажав на кнопку ниже.", reply_markup=keyboard)

# Обработка местоположения пользователя


@dp.message_handler(content_types=types.ContentType.LOCATION)
async def handle_location(message: types.Message):
    latitude = message.location.latitude
    longitude = message.location.longitude
    telegram_id = message.from_user.id
    # Проверка наличия username
    username = message.from_user.username if message.from_user.username else None

    # Отправляем координаты и username на сервер Django для обновления
    data = {
        "telegram_id": telegram_id,
        "username": username,
        "location": {
            "latitude": latitude,
            "longitude": longitude
        }
    }
    response = requests.post(DJANGO_API_URL, json=data)

    if response.status_code == 200:
        await message.answer("Ваше местоположение и имя пользователя успешно обновлены.")
    else:
        await message.answer("Ошибка при обновлении данных.")
