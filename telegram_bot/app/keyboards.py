from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

booking = InlineKeyboardMarkup(inline_keyboard=[
	[InlineKeyboardButton(text='Начать бронирование', callback_data='start_booking')]
])

location = ReplyKeyboardMarkup(keyboard=[
	[KeyboardButton(text='Отправить локацию',  request_location=True)]
], resize_keyboard=True)
