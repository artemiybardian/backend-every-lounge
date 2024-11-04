# import asyncio
# from aiogram import Bot, Dispatcher, types, F
# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
# from aiogram.filters import CommandStart
# from aiogram.types import Location
# import requests
# import logging

# # Настройка логирования
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# API_TOKEN = '7702184372:AAFpYNtn0V1MJRYB7BwgYVkd1pBhdWvSXCU'
# DJANGO_API_URL = 'https://127.0.0.1:8000/api/users/auth/'

# bot = Bot(token=API_TOKEN)
# dp = Dispatcher()

# # Обработка команды /start


# @dp.message(CommandStart())
# async def send_welcome(message: types.Message):
#     logger.info("Команда /start получена от %s", message.from_user.username)

#     location_button = KeyboardButton(
#         text="Отправить своё местоположение", request_location=True)
#     keyboard = ReplyKeyboardMarkup(
#         keyboard=[[location_button]],
#         resize_keyboard=True
#     )

#     await message.answer("Пожалуйста, отправьте своё текущее местоположение, нажав на кнопку ниже.", reply_markup=keyboard)

# # Обработка местоположения пользователя


# @dp.message(F.content_type(types.ContentType.LOCATION))
# async def handle_location(message: types.Message):
#     logger.info("Получено местоположение от пользователя")
#     latitude = message.location.latitude
#     longitude = message.location.longitude
#     telegram_id = message.from_user.id
#     username = message.from_user.username
#     first_name = message.from_user.first_name if message.from_user.first_name else None
#     last_name = message.from_user.last_name if message.from_user.last_name else None

#     data = {
#         "telegram_id": telegram_id,
#         "username": username,
#         "first_name": first_name,
#         "last_name": last_name,
#         "location": {
#             "latitude": latitude,
#             "longitude": longitude
#         }
#     }

#     response = requests.post(DJANGO_API_URL, json=data)
#     logger.info("Отправлены данные на Django: %s", data)

#     if response.status_code == 200:
#         await message.answer("Ваши данные успешно обновлены.")
#     else:
#         await message.answer("Ошибка при обновлении данных.")

# # Логика запуска бота


# async def main():
#     logger.info("Запуск бота...")
#     await dp.start_polling(bot, skip_updates=True)

# if __name__ == '__main__':
#     asyncio.run(main())
