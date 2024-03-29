from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command="read_last", description="Вивести останнє повідомлення з бази даних"
        ),
        BotCommand(
            command="test_kb", description="Виводить тестову інлайн клавіатуру № 1"
        ),
        BotCommand(
            command="test2_kb", description="Виводить тестову інлайн клавіатуру № 2"
        ),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
