import asyncio
import os

from aiogram import Dispatcher, Bot
from redis.asyncio.client import Redis

from settings import BOT_TOKEN
import logging
from handlers import echo, inline_kb
from utils.commands import set_commands
from aiogram.fsm.storage.redis import RedisStorage
from create_bot import bot, dp


async def main():
    """ Функція запуску бота"""
    logging.basicConfig(level=logging.INFO)
    # bot = Bot(token=BOT_TOKEN)
    await set_commands(bot)
    # redis = Redis(
    #     port=os.environ.get('REDIS_PORT'),
    #     host=os.environ.get('REDIS_HOST')
    # )
    # dp = Dispatcher(storage=RedisStorage(redis=redis))
    dp.include_router(inline_kb.router)
    dp.include_router(echo.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
