from utils.database_functions.get_from_db import user_is_in_database
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware, types
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder


class UserInDatabaseMiddleware(BaseMiddleware):
    """Middleware, що перевіряє наявність користувача в базі даних та підтримує процес реєстрації користувача.
    Реагує на Message."""
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:

        # Якщо користувач натискає кнопку "Відмінити реєстрацію" перериваємо опрацювання
        if event.text == "Скасувати реєстрацію":
            return event.answer("До зустрічі!", reply_markup=types.ReplyKeyboardRemove())

        # Якщо користувач є в базі даних, або надсилає повідомлення в групі продовжуємо опрацювання івенту
        # При надсиланні контакту користувачем також продовжуємо опрацювання
        if event.chat.type == 'group' or user_is_in_database(event.from_user.id) or event.contact:
            return await handler(event, data)

        # Якщо користувача немає в базі даних, то опрацювання переривається. Пропонується реєстрація
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(text="Зареєструватись", callback_data="registration"))

        await event.answer(
            f"Привіт, {event.from_user.full_name}!\n"
            "Щоб скористатись моїми послугами потрібно зареєструватись.\n",
            reply_markup=builder.as_markup())
        return
