from aiogram import Router, types
from aiogram.filters import Text
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from utils.database_functions.get_from_db import add_guest_to_db
from aiogram import F
from keyboards.registration_kb import get_accept_kb, get_contact_kb

router = Router()


class StepsForm(StatesGroup):
    SEND_NAME = State()
    SEND_LAST_NAME = State()
    SEND_EMAIL = State()
    WAIT_CONTACT = State()
    FINISH_STATE = State()


@router.callback_query(Text(text="registration"))
async def cmd_start(callback: CallbackQuery, state: FSMContext):
    """Хендлер, що ловить колбек при натисканні кнопки реєстрація від користувача"""
    await callback.message.answer(
        f"Чудово!\n"
        "Тепер надішли мені свій номер. Або можеш все відмінити.\n",
        reply_markup=get_contact_kb())
    await callback.answer()
    await state.set_state(StepsForm.WAIT_CONTACT)


@router.message(StepsForm.WAIT_CONTACT, F.contact)
async def get_name(message: Message, state: FSMContext):
    user_data = {
        "id": message.contact.user_id,
        "first_name": message.contact.first_name,
        "last_name": message.contact.last_name,
        "email": "N/A",
        "phone": message.contact.phone_number,
    }
    await add_guest_to_db(message.contact)

    out_data = "\n".join([str(key) + ": " + str(value) for key, value in user_data.items()])
    await message.reply("Дякую!", reply_markup=types.ReplyKeyboardRemove())
    await message.answer("Залишити ці дані чи бажаєте щось змінити?\n" + out_data,
                         reply_markup=get_accept_kb())
    # await state.set_state(StepsForm.FINISH_STATE)


# # @router.message(StepsForm.GET_NAME)
# # async def get_name(message: Message, state: FSMContext):
# #     await message.answer(f'твое имя:\n{message.text}\nТеперь введи фамилию:')
# #     await state.update_data(name=message.text)
# #     await state.set_state(StepsForm.GET_SECOND_NAME)
#
# @router.message(StepsForm.GET_SECOND_NAME)
# async def get_name(message: Message, state: FSMContext):
#     await message.answer(f'твоя фамилия:\n{message.text}\nТеперь введи свой номер телефона:')
#     await state.update_data(second_name=message.text)
#     await state.set_state(StepsForm.GET_PHONE)
#
#
# @router.message(StepsForm.GET_PHONE)
# async def get_name(message: Message, state: FSMContext):
#     await message.answer(f'твой номер телефона:\n{message.text}\nТеперь проверь свои данные:')
#     context_data = await state.get_data()
#     # await message.answer(f'сохраненные данные в машине сосотояний:\r\n{str(context_data)}')
#     name = context_data.get('name')
#     second_name = context_data.get('second_name')
#     data_user = f'имя: {name}\n' \
#                 f'фамилия: {second_name}\n' \
#                 f'телефон: {message.text}\n'
#
#
#     builder = InlineKeyboardBuilder()
#     builder.add(types.InlineKeyboardButton(
#         text="подтверждаю", callback_data="hi")
#         )
#     await message.answer(
#         data_user,
#         reply_markup=builder.as_markup()
#         )
#
#     await state.clear()
#
#
# @router.message(Text(text="выход"))
# async def cmd_start(message: Message):
#     await message.answer(f"До встречи {message.from_user.username}")