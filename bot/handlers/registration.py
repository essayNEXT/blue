from aiogram import Router, types
from aiogram.filters import Text
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

router = Router()


class StepsForm(StatesGroup):
    GET_NAME = State()
    GET_SECOND_NAME = State()
    GET_PHONE = State()


@router.callback_query(Text(text="registration"))
async def cmd_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(f"Начнем регистрацию\nВведи свое имя:")
    await state.set_state(StepsForm.GET_NAME)


@router.message(StepsForm.GET_NAME)
async def get_name(message: Message, state: FSMContext):
    await message.answer(f'твое имя:\n{message.text}\nТеперь введи фамилию:')
    await state.update_data(name=message.text)
    await state.set_state(StepsForm.GET_SECOND_NAME)


@router.message(StepsForm.GET_SECOND_NAME)
async def get_name(message: Message, state: FSMContext):
    await message.answer(f'твоя фамилия:\n{message.text}\nТеперь введи свой номер телефона:')
    await state.update_data(second_name=message.text)
    await state.set_state(StepsForm.GET_PHONE)


@router.message(StepsForm.GET_PHONE)
async def get_name(message: Message, state: FSMContext):
    await message.answer(f'твой номер телефона:\n{message.text}\nТеперь проверь свои данные:')
    context_data = await state.get_data()
    # await message.answer(f'сохраненные данные в машине сосотояний:\r\n{str(context_data)}')
    name = context_data.get('name')
    second_name = context_data.get('second_name')
    data_user = f'имя: {name}\n' \
                f'фамилия: {second_name}\n' \
                f'телефон: {message.text}\n'


    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="подтверждаю", callback_data="hi")
        )
    await message.answer(
        data_user,
        reply_markup=builder.as_markup()
        )

    await state.clear()


@router.message(Text(text="выход"))
async def cmd_start(message: Message):
    await message.answer(f"До встречи {message.from_user.username}")