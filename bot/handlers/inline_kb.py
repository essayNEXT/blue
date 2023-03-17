from aiogram import Router
from aiogram.utils.keyboard import InlineKeyboardButton
from aiogram.filters import Command, Text
from aiogram.types import Message, CallbackQuery
from keyboards.inline import CombineInlineKeyboardGenerator
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


class InlineStates(StatesGroup):
    Inline = State()


router = Router()


@router.message(Command(commands='inline_kb'))
async def get_inline_kb(event: Message, state: FSMContext):
    """Хендлер реагує на команду /inline_kb та створює об'єкт інлайн клавіатури.
    Клавіатура складається з 20 скролінгових кнопок та двох статичних.
    Максимальна кількість видимих скролінг кнопок визначається при створенні об'єкта CombineInlineKeyboardGenerator.
    Екземпляр клавіатури тимчасово зберігається в сховищі стану. Далі буде реалізоване інше сховище."""
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
    kb_data = {"keyboard": kb}

    await state.set_data(kb_data)
    print(event.from_user.language_code)
    await event.answer("Це твоя інлайн клавіатура",
                       reply_markup=kb.markup())


@router.callback_query(Text(text="keyboard_down"))
async def down_button(event: CallbackQuery, state: FSMContext):
    """Хендлер відловлює колбек кнопки 'вниз'. Витягує зі сховища об'єкт клавіатури.
    При натисканні кнопки 'вниз' переходить на наступний рівень пагінації викликом функції markup_down."""
    kb_data = await state.get_data()
    kb = kb_data['keyboard']
    await event.message.edit_text("Клавіатура після кнопки вниз",
                                  reply_markup=kb.markup_down())
    kb_data = {"keyboard": kb}
    await state.set_data(kb_data)


@router.callback_query(Text(text="keyboard_up"))
async def down_button(event: CallbackQuery, state: FSMContext):
    """Хендлер відловлює колбек кнопки 'вверх'. Витягує зі сховища об'єкт клавіатури.
    При натисканні кнопки 'вверх' переходить на попередній рівень пагінації викликом функції markup_down."""
    kb_data = await state.get_data()
    kb = kb_data['keyboard']
    await event.message.edit_text("Клавіатура після кнопки вверх",
                                  reply_markup=kb.markup_up())
    kb_data = {"keyboard": kb}
    await state.set_data(kb_data)
