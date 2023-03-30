from typing import Union
from aiogram import Router
from aiogram.filters import Command, Text
from aiogram.types import Message, CallbackQuery
from keyboards.inline import KeyKeyboard, MyContextUserKeyboard, MyKeyboard
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from utils.storages import TmpStorage
from create_bot import bot


class InlineStates(StatesGroup):
    Inline = State()


router = Router()


@router.callback_query(Text(startswith="scroll_"))
@router.callback_query(Text(startswith="inline_button_"))
@router.callback_query(Text(startswith="top_button_"))
@router.callback_query(Text(startswith="bottom_button_"))
@router.message(Command(commands='inline_kb'))
async def get_inline_kb(event: Union[Message, CallbackQuery], state: FSMContext, tmp_storage: TmpStorage):
    """Хендлер реагує на команду /inline_kb та створює об'єкт інлайн клавіатури.
    Клавіатура складається зі скролінгових кнопок та верхніх і нижніх статичних.
    Максимальна кількість 'видимих' скролінг кнопок визначається при створенні об'єкта CombineInlineKeyboardGenerator.
    Екземпляр клавіатури тимчасово зберігається в сховищі tmp_storage: TmpStorage диспетчера.

    Хендлер відловлює колбек кнопки 'вниз'. Витягує зі сховища об'єкт клавіатури.
    При натисканні кнопки 'вниз' переходить на наступний рівень пагінації викликом функції markup_down.

    Хендлер відловлює колбек кнопки 'вверх'. Витягує зі сховища об'єкт клавіатури.
    При натисканні кнопки 'вверх' переходить на попередній рівень пагінації викликом функції markup_up."""
    if isinstance(event, Message):
        print(f"tmp_storage: {tmp_storage}")
        print(f"type of tmp_storage: {type(tmp_storage)}")
        print(f"id of tmp_storage: {id(tmp_storage)}")
        await state.set_state(InlineStates.Inline)

        kb = MyContextUserKeyboard(
            max_rows_number=4,
            scroll_step=1,
            user_language="en"
        )
        key = KeyKeyboard(
            bot_id=bot.id,
            chat_id=event.chat.id,
            user_id=event.from_user.id if event.from_user else None,
            message_id=event.message_id
        )
        print(f"key for keyboard is {key}")
        tmp_storage[key] = kb
        print(f"tmp_storage after add kb: {tmp_storage}")
        await event.answer("Це твоя інлайн клавіатура",
                           reply_markup=tmp_storage[key].markup())
    elif isinstance(event, CallbackQuery):
        key = KeyKeyboard(
            bot_id=bot.id,
            chat_id=event.message.chat.id,
            user_id=event.from_user.id if event.from_user else None,
            message_id=event.message.message_id - 1
        )
        print(f"key for keyboard is {key}")

        message_text = tmp_storage[key].context_callback_message(event)
        if event.data == "scroll_down":
            reply_markup = tmp_storage[key].markup_down()
        elif event.data == "scroll_up":
            reply_markup = tmp_storage[key].markup_up()
        else:
            reply_markup = tmp_storage[key].markup()
        await event.message.edit_text(message_text, reply_markup=reply_markup)


@router.message(Command(commands='test_kb'))
@router.callback_query(Text(startswith="button_"))
async def get_test_kb(event: Union[Message, CallbackQuery], state: FSMContext, tmp_storage: TmpStorage):
    """Хендлер для тестової клавіатури MyKeyboard"""
    if isinstance(event, Message):
        await state.set_state(InlineStates.Inline)

        kb = MyKeyboard(user_language="ja")

        key = KeyKeyboard(
            bot_id=bot.id,
            chat_id=event.chat.id,
            user_id=event.from_user.id if event.from_user else None,
            message_id=event.message_id
        )
        tmp_storage[key] = kb
        await event.answer(kb.text, reply_markup=kb.markup())

    if isinstance(event, CallbackQuery):
        key = KeyKeyboard(
            bot_id=bot.id,
            chat_id=event.message.chat.id,
            user_id=event.from_user.id if event.from_user else None,
            message_id=event.message.message_id - 1
        )
        kb = tmp_storage[key]
        kb.callback(event)
        await event.message.edit_text(kb.text, reply_markup=kb.markup())
