from utils.database_functions.get_from_db import is_in_database
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware, types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


class UserInDatabaseMiddleware(BaseMiddleware):
    """Мідлварь, який перевіряє наявність користувача в базі даних"""
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        # Якщо користувач є в базі даних, або надсилає повідомлення в групі продовжуємо опрацювання апдейту
        if event.chat.type == 'group' or is_in_database(event.from_user.id):
            return await handler(event, data)
        # Якщо користувача немає в базі даних, то опрацювання переривається. Пропонується реєстрація
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(
            text="Зареєструватись",
            callback_data="registration")
        )
        await event.answer(
            f"Привіт, {event.from_user.full_name}!\n"
            "Щоб скористатись моїми послугами потрібно зареєструватись.\n",
            reply_markup=builder.as_markup()
        )
        return
