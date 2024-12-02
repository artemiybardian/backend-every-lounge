import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from app.handlers import router as app_router


logging.basicConfig(level=logging.INFO)
log = logging.getLogger('Bot')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def main():
    dp.include_router(app_router)
    await dp.start_polling(bot)
    log.info('Бот запустился')

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info('Exit')
