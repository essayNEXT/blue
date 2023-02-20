import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from settings import BOT_TOKEN
from aiogram.filters import Command


logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher()


@dp.message(Command(commands=["start"]))
async def cmd_start(message: Message):
    await message.answer("Hello!")


@dp.message()
async def cmd_start(message: Message):
    await message.answer(f"Від користувача - {message.from_user.id}\n"
                         f"{message.text}")


# Запуск бота
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
