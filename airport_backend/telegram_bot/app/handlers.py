from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from app.keyboards import booking, location
from config import DJANGO_API_URL, WEBAPP_URL
import logging
import requests

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('Handlers')


router = Router()


@router.message(CommandStart())
async def start(message: Message):
    welcome_text = (
        "✈️ **Добро пожаловать в Every Lounge WebApp!**\n\n"
        "Забронируйте доступ в лучшие залы ожидания аэропортов по всему миру."
        "Просто следуйте инструкциям, и мы подберем для вас ближайший доступный зал.\n\n"
        "Нажмите **'Начать бронирование'**, чтобы продолжить!"
    )
    
    await message.answer(text=welcome_text, reply_markup=booking, parse_mode='Markdown')
    log.info(f'Обработана команда /start')


@router.callback_query(F.data == 'start_booking')
async def start_booking(callback: CallbackQuery):
    first_text = "📍 **Пожалуйста, отправьте ваше местоположение, чтобы мы нашли ближайшие залы ожидания!**"
    second_text = "Нажмите **'Отправить локацию'**, чтобы продолжить!"
    await callback.answer('Вы начали бронирование!')
    await callback.message.edit_text(text=first_text, parse_mode='Markdown')
    await callback.message.answer(text=second_text, reply_markup=location, parse_mode='Markdown')


@router.message(F.location)
async def handle_location(message: Message):
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
    
    response = requests.post(DJANGO_API_URL, json=data)
    log.info("Отправлены данные на Django: %s", data)

    if response.status_code == 200:
        # Получаем токен доступа из Django API
        response_data = response.json()
        if 'token' in response_data:
            access_token = response_data['token']

            # Создаем кнопку для перехода в WebApp с передачей токена
            lounge_book = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Забронировать зал😊", 
                                      web_app=WebAppInfo(
                                          url=f"{WEBAPP_URL}?token={access_token}"))]
            ])

            await message.answer("Бронируйте залы ожидания аэропортов по кнопке ниже:", reply_markup=lounge_book)

        else:
            message.answer("Не удалось получить токен. Попробуйте еще раз.")
            log.error("Не удалось получить токен")
    else:
        message.answer("Ошибка при получении данных.")
        log.error("Ошибка при получении данных.")
