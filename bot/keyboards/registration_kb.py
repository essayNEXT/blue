from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_contact_kb() -> ReplyKeyboardMarkup:
    """Клавіатура виводиться в меню при натисканні кнопки 'зареєструватись'."""
    kb = ReplyKeyboardBuilder()
    kb.button(text="Надіслати свій контакт", request_contact=True)
    kb.button(text="Скасувати реєстрацію")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True, input_field_placeholder="Оберіть відповідь", one_time_keyboard=True)


def get_accept_kb() -> InlineKeyboardMarkup:
    """Інлайн-клавіатура виводиться в повідомленні після надсилання контакту або після зміни даних."""
    kb = InlineKeyboardBuilder()
    kb.button(text="Залишити", callback_data="confirm")
    kb.button(text="Змінити", callback_data="change")
    return kb.as_markup()


def get_change_kb() -> InlineKeyboardMarkup:
    """Інлайн-клавіатура виводиться в повідомленні після натискання кнопки 'змінити'."""
    kb = InlineKeyboardBuilder()
    kb.button(text="Ім'я", callback_data="change_first_name")
    kb.button(text="Прізвище", callback_data="change_last_name")
    kb.button(text="Email", callback_data="change_email")
    kb.button(text="Номер телефону", callback_data="change_phone")
    kb.adjust(2)
    return kb.as_markup()
