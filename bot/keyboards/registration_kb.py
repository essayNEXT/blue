from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_contact_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Надіслати свій номер телефону", request_contact=True)
    kb.button(text="Відмінити реєстрацію")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True, input_field_placeholder="Оберіть відповідь")


def get_accept_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Залишити", callback_data="confirm")
    kb.button(text="Змінити", callback_data="change")
    return kb.as_markup()
