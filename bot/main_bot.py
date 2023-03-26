import asyncio
import logging
from handlers import echo, inline_kb
from utils.commands import set_commands
from create_bot import bot, dp


async def main():
    """Функція запуску бота"""
    logging.basicConfig(level=logging.INFO)
    await set_commands(bot)
    dp.include_router(inline_kb.router)
    dp.include_router(echo.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
