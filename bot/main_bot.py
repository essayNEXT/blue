import asyncio
from aiogram import Dispatcher, Bot
from settings import BOT_TOKEN
import logging
from handlers import echo


async def main():
    """ Функція запуска бота"""
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token= BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(echo.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
