from aiogram import Router
from aiogram.utils.keyboard import InlineKeyboardButton
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.inline import CombineInlineKeyboardGenerator
from aiogram.fsm.state import State
from



router = Router()


@router.message(Command(commands='inline_kb'))
async def get_inline_kb(event: Message):
    num_of_scrolls = 8
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
    await event.answer("Це твоя інлайн клавіатура",
                       reply_markup=kb.markup())
