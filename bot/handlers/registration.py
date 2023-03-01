from aiogram import Router
from aiogram.filters import Text
from aiogram.types import CallbackQuery

router = Router()


@router.callback_query(Text(text="registration"))
async def checkin_confirm(callback: CallbackQuery):
    """Попередній хендлер, що відловлює колбек від користувача при реєстрації"""
    await callback.answer()
    await callback.message.answer(
        "Дякую за реєстрацію!"
    )
