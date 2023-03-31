from typing import Union
from aiogram import Router
from aiogram.filters import Command, Text
from aiogram.types import Message, CallbackQuery
from keyboards.inline import KeyKeyboard, MyKeyboard
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from utils.storages import TmpStorage
from create_bot import bot


class InlineStates(StatesGroup):
    Inline = State()


router = Router()


@router.message(Command(commands='test_kb'))
@router.callback_query(Text(startswith="#_test_"))
async def get_test_kb(event: Union[Message, CallbackQuery], state: FSMContext, tmp_storage: TmpStorage):
    """Хендлер для тестової клавіатури MyKeyboard"""
    if isinstance(event, Message):
        await state.set_state(InlineStates.Inline)

        # user_language = event.from_user.language_code
        user_language = "en"
        kb = MyKeyboard(user_language=user_language)

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
        if event.data == "#_test_scroll_up":
            kb.markup_up()
        elif event.data == "#_test_scroll_down":
            kb.markup_down()
        else:
            kb.callback(event)

        await event.message.edit_text(kb.text, reply_markup=kb.markup())
