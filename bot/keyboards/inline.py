from typing import List, Optional
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from dataclasses import dataclass

from .temp_buttons import temp_top_static_buttons, temp_scroll_keys, temp_bottom_static_buttons, get_inline_buttons_list


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
            top_static_buttons: Optional[List[List[InlineKeyboardButton]]] = None,
            bottom_static_buttons: Optional[List[List[InlineKeyboardButton]]] = None,
            max_rows_number: int = 5,
            start_row: int = 0,
            scroll_step: int = 1,
            user_language: str = "en"
    ) -> None:
        super().__init__(scroll_keys, max_rows_number, start_row, scroll_step)
        if not top_static_buttons:
            top_static_buttons = []
        self.top_static_buttons = top_static_buttons
        if not bottom_static_buttons:
            bottom_static_buttons = []
        self.bottom_static_buttons = bottom_static_buttons
        # перевіряємо чи є мова користувача в списку підтримуваних
        self.user_language = user_language if user_language in supported_languages else "en"

    def markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=self.top_static_buttons + self._get_current_scroll_keyboard_list()
                            + self.bottom_static_buttons
        )

    def update_keyboard_to_user_language(
            self,
            top_static_buttons,
            scroll_keys,
            down_static_buttons,
    ):
        pass


class ContextUserKeyboard(CombineInlineKeyboardGenerator):
    """Клас, що описує конкретну клавіатуру користувача.
    В даному класі описуються функції, що повертають параметри обробки колбеку для кожної кнопки."""

    def __init__(
            self,
            scroll_keys: List[List[InlineKeyboardButton]] = get_inline_buttons_list(temp_scroll_keys, 'uk'),
            top_static_buttons: Optional[List[List[InlineKeyboardButton]]] = get_inline_buttons_list(temp_top_static_buttons, 'uk'),
            bottom_static_buttons: Optional[List[List[InlineKeyboardButton]]] = get_inline_buttons_list(temp_bottom_static_buttons, 'uk'),
            max_rows_number: int = 5,
            start_row: int = 0,
            scroll_step: int = 1,
            user_language: str = 'en'
    ) -> None:
        super().__init__(scroll_keys, top_static_buttons, bottom_static_buttons,
                         max_rows_number, start_row, scroll_step, user_language)


supported_languages = ["en", "uk", "ru"]


