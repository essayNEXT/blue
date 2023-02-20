import asyncio
import logging
from aiogram import Bot, Dispatcher
from blue.config_reader import config
from handlers import message_handlers


# Запуск бота
async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=config.bot_token.get_secret_value(), parse_mode='HTML')
    dp = Dispatcher()

    dp.include_router(message_handlers.router)
    # Запускаємо бота и пропускаємо всі накопичені вхідні повідомлення
    # Так, так цей метод можна запускати навіть при полінгу
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
