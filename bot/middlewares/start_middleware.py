from utils.database_functions.get_from_db import is_in_database
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message


class UserInDatabaseMiddleware(BaseMiddleware):
    """Мідлварь, який перевіряє наявність користувача в базі даних"""
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        # Якщо користувача немає в базі даних продовжуємо опрацювання апдейту
        if is_in_database(event.from_user.id):
            return await handler(event, data)
        # Якщо користувач є в базі даних, то опрацювання переривається
        await event.answer(
            f"Привіт, {event.from_user.full_name}!\n"
            "Щоб скористатись моїми послугами потрібно зареєструватись.\nЦе легко)\n"
            "[Кнопка реєстрації]"
        )
        return
