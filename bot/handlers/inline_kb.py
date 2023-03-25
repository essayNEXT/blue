from typing import Union
from aiogram import Router
from aiogram.utils.keyboard import InlineKeyboardButton
from aiogram.filters import Command, Text
from aiogram.types import Message, CallbackQuery
from keyboards.inline import CombineInlineKeyboardGenerator, KeyKeyboard
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from utils.storages import TmpStorage
from create_bot import bot, dp


class InlineStates(StatesGroup):
    Inline = State()


router = Router()


@router.callback_query(Text(startswith="inline_keyboard_"))
@router.message(Command(commands='inline_kb'))
async def get_inline_kb(event: Union[Message, CallbackQuery], state: FSMContext, tmp_storage: TmpStorage):
    """Хендлер реагує на команду /inline_kb та створює об'єкт інлайн клавіатури.
    Клавіатура складається з 20 скролінгових кнопок та двох статичних.
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
        num_of_scrolls = 20
        scroll_key_buttons = [
            [
                InlineKeyboardButton(
                    text=f"Inline button {button}",
                    callback_data=f"inline_button_{button}"
                )
            ] for button in range(1, num_of_scrolls + 1)
        ]

        additional_buttons = [
            [
                InlineKeyboardButton(
                    text="Additional button 1",
                    callback_data="additional_button_1"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Additional button 2",
                    callback_data="additional_button_2"
                ),
            ]
        ]

        kb = CombineInlineKeyboardGenerator(
            scroll_keys=scroll_key_buttons,
            additional_buttons_list=additional_buttons,
            max_rows_number=5,
            scroll_step=1
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
        if event.data == "inline_keyboard_down":
            message_text = "Клавіатура після кнопки вниз"
            reply_markup = tmp_storage[key].markup_down()
        elif event.data == "inline_keyboard_up":
            message_text = "Клавіатура після кнопки вверх"
            reply_markup = tmp_storage[key].markup_up()
        await event.message.edit_text(message_text, reply_markup=reply_markup)
