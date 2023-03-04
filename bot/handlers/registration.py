from aiogram import Router, types
from aiogram.filters import Text
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from utils.database_functions.get_from_db import add_guest_to_db, update_guest_in_db
from aiogram import F
from keyboards.registration_kb import get_accept_kb, get_contact_kb, get_change_kb

router = Router()


class StepsForm(StatesGroup):
    INITIAL_DATA = State()
    CHANGE_DATA = State()
    CONFIRM_DATA = State()
    F_NAME_CHANGED = State()
    L_NAME_CHANGED = State()
    EMAIL_CHANGED = State()
    PHONE_CHANGED = State()


@router.callback_query(Text(text="registration"))
async def cmd_start(callback: CallbackQuery, state: FSMContext):
    """Хендлер, що ловить колбек при натисканні кнопки реєстрація від користувача"""
    await callback.message.answer(
        f"Чудово!\n"
        "Тепер надішли мені свій номер. Або можеш все відмінити.\n",
        reply_markup=get_contact_kb())
    await callback.answer()
    await state.set_state(StepsForm.INITIAL_DATA)


@router.message(StepsForm.INITIAL_DATA, F.contact)
@router.message(StepsForm.F_NAME_CHANGED)
@router.message(StepsForm.L_NAME_CHANGED)
@router.message(StepsForm.PHONE_CHANGED)
@router.message(StepsForm.EMAIL_CHANGED)
async def confirm_data(message: Message, state: FSMContext):
    user_state = await state.get_state()

    if user_state == StepsForm.INITIAL_DATA:
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

    await state.set_state(StepsForm.CONFIRM_DATA)

    out_data = "\n".join([str(key) + ": " + str(value) for key, value in user_data.items()])
    await message.answer("<b>Ваші облікові дані</b>\n" +
                         out_data + "\nЗалишити ці дані чи бажаєте щось змінити?\n",
                         reply_markup=get_accept_kb())


@router.callback_query(StepsForm.CONFIRM_DATA, Text(text="confirm"))
async def get_name(callback: CallbackQuery, state: FSMContext):
    """Хендлер, що ловить колбек при натисканні кнопки Залишити від користувача"""
    await callback.answer()
    user_data = await state.get_data()
    await update_guest_in_db(callback.from_user.id, user_data)
    await callback.message.answer(f"Ви зареєстровані! Вітаю!")
    await state.clear()


@router.callback_query(StepsForm.CONFIRM_DATA, Text(text="change"))
async def get_name(callback: CallbackQuery, state: FSMContext):
    """Хендлер, що ловить колбек при натисканні кнопки Змінити від користувача"""
    await callback.answer()
    await callback.message.answer(f"Що саме бажаєте змінити?", reply_markup=get_change_kb())
    await state.set_state(StepsForm.CHANGE_DATA)


@router.callback_query(StepsForm.CHANGE_DATA, Text(startswith="change_"))
async def get_name(callback: CallbackQuery, state: FSMContext):
    """Хендлер, що ловить колбек при натисканні кнопки зміни визначеного атрибута від користувача"""
    await callback.answer()

    if callback.data == "change_first_name":
        await callback.message.answer("Введи ім'я:")
        await state.set_state(StepsForm.F_NAME_CHANGED)
    elif callback.data == "change_last_name":
        await callback.message.answer("Введіть прізвище:")
        await state.set_state(StepsForm.L_NAME_CHANGED)
    elif callback.data == "change_email":
        await callback.message.answer("Введіть свій email:")
        await state.set_state(StepsForm.EMAIL_CHANGED)
    elif callback.data == "change_phone":
        await callback.message.answer("Введіть свій номер телефону:")
        await state.set_state(StepsForm.PHONE_CHANGED)
