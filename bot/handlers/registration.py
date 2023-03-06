from aiogram import F
from aiogram import Router
from aiogram.filters import Text
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from utils.database_functions.get_from_db import add_guest_to_db, update_guest_in_db
from keyboards.registration_kb import get_accept_kb, get_contact_kb, get_change_kb
from encodings import utf_8

router = Router()


class StepsForm(StatesGroup):
    """Клас, що описує стани проходження реєстрації користувача."""
    INITIAL_DATA = State()
    CHANGE_DATA = State()
    CONFIRM_DATA = State()
    F_NAME_CHANGED = State()
    L_NAME_CHANGED = State()
    EMAIL_CHANGED = State()
    PHONE_CHANGED = State()


@router.callback_query(Text(text="registration"))
async def cmd_start(callback: CallbackQuery, state: FSMContext):
    """Хендлер, що ловить колбек при натисканні кнопки 'Зареєструватись' від користувача.
    Повертає реквест-кнопки клавіатури:
    1. надіслати контакт
    2. скасувати реєстрацію"""
    # Видаляємо кнопку реєстрації, щоб користувач не міг натискати її безліч разів
    await callback.message.delete()
    await callback.message.answer(
        f"Чудове рішення, {callback.from_user.first_name}!\n"
        "Тепер надішли мені свій контакт або можеш все скасувати.\n",
        reply_markup=get_contact_kb())
    await state.set_state(StepsForm.INITIAL_DATA)


@router.message(StepsForm.INITIAL_DATA, F.contact)
@router.message(StepsForm.F_NAME_CHANGED)
@router.message(StepsForm.L_NAME_CHANGED)
@router.message(StepsForm.PHONE_CHANGED)
@router.message(StepsForm.EMAIL_CHANGED)
async def confirm_data(message: Message, state: FSMContext):
    """Хендлер, що обробляє контактні дані, отримані від користувача, та виводить на погодження.
    При першому надсиланні контакту обробляє дані та заносить в дані стану.
    При подальшій зміні даних змінює дані стану.
    Виводить колбек-кнопки 'змінити' та 'залишити'."""
    user_state = await state.get_state()
    if user_state == StepsForm.INITIAL_DATA:
        await message.answer("Контакт отримано!", reply_markup=ReplyKeyboardRemove())
        user_data = {
            "user_id": message.contact.user_id,
            "first_name": message.contact.first_name,
            "last_name": message.contact.last_name,
            "email": "N/A",
            "phone": message.contact.phone_number,
        }
        await state.set_data(user_data)
        await add_guest_to_db(message.contact)

    elif user_state == StepsForm.F_NAME_CHANGED:
        user_data = await state.update_data(first_name=message.text)
        await message.answer("Ім'я змінено!")

    elif user_state == StepsForm.L_NAME_CHANGED:
        user_data = await state.update_data(last_name=message.text)
        await message.answer("Прізвище змінено!")

    elif user_state == StepsForm.EMAIL_CHANGED:
        user_data = await state.update_data(email=message.text)
        await message.answer("Email змінено!")

    elif user_state == StepsForm.PHONE_CHANGED:
        user_data = await state.update_data(phone=message.text)
        await message.answer("Телефон змінено!")

    # змінюємо стан на 'підтвердження даних'
    await state.set_state(StepsForm.CONFIRM_DATA)
    # формуємо вихідні дані користувача для виводу
    out_data = "\n".join([str(key) + ": " + str(value) for key, value in user_data.items()])
    await message.answer("<b>Ваші облікові дані:</b>\n" + out_data +
                         "\n\n<b><u>Залишити ці дані чи бажаєте щось змінити?</u></b>\n",
                         reply_markup=get_accept_kb())


@router.callback_query(StepsForm.CONFIRM_DATA, Text(text="confirm"))
async def get_name(callback: CallbackQuery, state: FSMContext):
    """Хендлер, що ловить колбек при натисканні кнопки Залишити від користувача.
    Остаточні дані від користувача заностяться до бази даних."""
    await callback.answer()
    user_data = await state.get_data()
    # заносимо отримані остаточні дані від користувача в базу даних
    await update_guest_in_db(callback.from_user.id, user_data)
    await callback.message.edit_text(f"Тебе зареєстровано! Вітаю 😉")
    await state.clear()


@router.callback_query(StepsForm.CONFIRM_DATA, Text(text="change"))
async def get_name(callback: CallbackQuery, state: FSMContext):
    """Хендлер, що ловить колбек при натисканні кнопки Змінити від користувача.
    Виводить колбек кнопки з варіантами зміни імені, прізвища, пошти та номеру телефону."""
    await callback.answer()
    user_data = await state.get_data()
    # формуємо вихідні дані користувача для виводу
    out_data = "\n".join([str(key) + ": " + str(value) for key, value in user_data.items()])
    await callback.message.edit_text("<b>Ваші облікові дані:</b>\n" + out_data + "\n\nЩо саме бажаєте змінити?",
                                     reply_markup=get_change_kb())
    await state.set_state(StepsForm.CHANGE_DATA)


@router.callback_query(StepsForm.CHANGE_DATA, Text(startswith="change_"))
async def get_name(callback: CallbackQuery, state: FSMContext):
    """Хендлер, що ловить колбек при натисканні кнопки зміни визначеного параметра від користувача.
    Виводить повідомляння з проханням вказати необхідний параметр та змінює стан згідно з параметром, що змінено."""
    await callback.answer()
    # перевіряємо вхідний колбек згідно з параметрами, які необхідно змінити
    if callback.data == "change_first_name":
        await callback.message.edit_text("Введи ім'я:")
        await state.set_state(StepsForm.F_NAME_CHANGED)
    elif callback.data == "change_last_name":
        await callback.message.edit_text("Введіть прізвище:")
        await state.set_state(StepsForm.L_NAME_CHANGED)
    elif callback.data == "change_email":
        await callback.message.edit_text("Введіть свій email:")
        await state.set_state(StepsForm.EMAIL_CHANGED)
    elif callback.data == "change_phone":
        await callback.message.edit_text("Введіть свій номер телефону:")
        await state.set_state(StepsForm.PHONE_CHANGED)
