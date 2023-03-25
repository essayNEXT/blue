from typing import List, Optional
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from dataclasses import dataclass


KEY_UP = InlineKeyboardButton(text="up", callback_data="inline_keyboard_up")
KEY_DOWN = InlineKeyboardButton(text="down", callback_data="inline_keyboard_down")


@dataclass(frozen=True)
class KeyKeyboard:
    """Описує ключ для ідентифікації примірника клавіатури та повідомлення"""

    __slots__ = ["bot_id", "chat_id", "user_id", "message_id"]

    bot_id: int
    chat_id: int
    user_id: int | None
    message_id: int


class ScrollInlineKeyboardGenerator:
    """Створює скролінг об'єкт клавіатури"""

    def __init__(
            self,
            scroll_keys: List[List[InlineKeyboardButton]],
            max_rows_number: int = 5,
            start_row: int = 0,
            scroll_step: int = 1
    ) -> None:
        self.scroll_keys = scroll_keys
        self.max_rows_number = max_rows_number
        self.start_row = start_row
        self.scroll_step = scroll_step

    def _get_current_scroll_keyboard_list(self) -> List[List[InlineKeyboardButton]]:
        """Повертає поточний список скролінгової клавіатури"""
        self.numbers_of_buttons_to_show = self.max_rows_number
        current_scroll_keyboard: List[List[InlineKeyboardButton]] = []
        if self.start_row != 0:
            current_scroll_keyboard = [[KEY_UP]] + current_scroll_keyboard
            self.numbers_of_buttons_to_show -= 1
        if self.start_row + self.numbers_of_buttons_to_show >= len(self.scroll_keys) - 1:
            return (
                current_scroll_keyboard
                + self.scroll_keys[
                    self.start_row:(self.start_row + self.numbers_of_buttons_to_show)
                ]
            )
        else:
            self.numbers_of_buttons_to_show -= 1
            return (
                current_scroll_keyboard
                + self.scroll_keys[
                    self.start_row: (self.start_row + self.numbers_of_buttons_to_show)
                ]
                + [[KEY_DOWN]]
            )

    def markup(self) -> InlineKeyboardMarkup:
        """Повертає теперішній стан скролінг клавіатури"""
        return InlineKeyboardMarkup(
            inline_keyboard=self._get_current_scroll_keyboard_list()
        )

    def markup_up(self) -> InlineKeyboardMarkup:
        """Повертає клавіатуру на 'один крок вперед'.

        Змінює значення внутрішніх змінних, які зберігаються в стані клавіатури після кроку 'вперед'
        і повертає новий об'єкт клавіатури.
        """
        self.start_row = (
            self.start_row -
            self.numbers_of_buttons_to_show if self.start_row - self.numbers_of_buttons_to_show >= 0 else 0
        )
        return self.markup()

    def markup_down(self) -> InlineKeyboardMarkup:
        """Повертає клавіатуру на 'один крок назад'.

        Змінює значення внутрішніх змінних, які зберігаються в стані клавіатури після кроку 'назад'
        і повертає новий об'єкт клавіатури.
        """
        self.start_row = (
            (self.start_row + self.numbers_of_buttons_to_show)
            if (self.start_row + (self.numbers_of_buttons_to_show - 1)) < len(self.scroll_keys)
            else len(self.scroll_keys) - self.numbers_of_buttons_to_show
        )
        return self.markup()


class CombineInlineKeyboardGenerator(ScrollInlineKeyboardGenerator):
    """Створює комбінований об'єкт клавіатури: скролінг та додаткові кнопки"""

    def __init__(
            self,
            scroll_keys: List[List[InlineKeyboardButton]],
            additional_buttons_list: Optional[List[List[InlineKeyboardButton]]] = None,
            max_rows_number: int = 5,
            start_row: int = 0,
            scroll_step: int = 1
    ) -> None:
        super().__init__(scroll_keys, max_rows_number, start_row, scroll_step)
        if not additional_buttons_list:
            additional_buttons_list = []
        self.additional_buttons_list = additional_buttons_list

    def markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=self._get_current_scroll_keyboard_list()
            + self.additional_buttons_list
        )
