from itertools import chain
from typing import List, Optional
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from dataclasses import dataclass
from aiogram.types import CallbackQuery

from .temp_buttons import context_button_set, context_button_set_languages, context_callback_messages
from .temp_buttons import default_buttons_messages

from utils.translate.kb_translate import translate_context


supported_languages = ["en", "uk", "ru"]


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
    KEY_UP = InlineKeyboardButton(text="up", callback_data="scroll_up")
    KEY_DOWN = InlineKeyboardButton(text="down", callback_data="scroll_down")

    def __init__(
            self,
            scroll_keys: List[List[InlineKeyboardButton]],
            max_rows_number: int = 5,
            start_row: int = 0,
            scroll_step: int = 1,
            user_language: str = "en"
    ) -> None:

        self.scroll_keys = scroll_keys
        self.max_rows_number = max_rows_number
        self.start_row = start_row
        self.scroll_step = scroll_step
        self.user_language = user_language if user_language in supported_languages else "en"

    def _get_current_scroll_keyboard_list(self) -> List[List[InlineKeyboardButton]]:
        """Повертає поточний список скролінгової клавіатури"""
        self.numbers_of_buttons_to_show = self.max_rows_number
        current_scroll_keyboard: List[List[InlineKeyboardButton]] = []
        if self.start_row != 0:
            current_scroll_keyboard = [[self.KEY_UP]] + current_scroll_keyboard
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
                    + [[self.KEY_DOWN]]
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

    def language_context_buttons(self, buttons_list: List[List[InlineKeyboardButton]], translate_data: dict):
        """Функція приймає об'єкти:
        - buttons_list: List[List[InlineKeyboardButton]] - список списків інлайн кнопок
        - translate_data: dict - словник з даними для перекладу
        Залежно від мови користувача повертає об'єкт List[List[InlineKeyboardButton]] адаптований
        до мови користувача"""
        if self.user_language == "en":
            return buttons_list
        else:
            new_buttons_list = []
            for raw in buttons_list:
                buttons_in_raw = []
                for single_button in raw:
                    single_button.text = translate_data[single_button.callback_data][self.user_language]
                    buttons_in_raw.append(single_button)
                new_buttons_list.append(buttons_in_raw)
            return new_buttons_list

    def language_context_text(self, callback_pattern: str, translate_data: dict):
        return translate_data[callback_pattern][self.user_language]


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
            inline_keyboard=list(chain(self.top_static_buttons,
                                       self._get_current_scroll_keyboard_list(),
                                       self.bottom_static_buttons))
        )


class ContextInlineKeyboardGenerator(CombineInlineKeyboardGenerator):
    """Клас-шаблон для створення клавіатури"""
    def __init__(
            self,
            user_language: str,
            kb_language: str,
            top_buttons: Optional[List[List[dict]]] = None,
            scroll_buttons: Optional[List[List[dict]]] = None,
            bottom_buttons: Optional[List[List[dict]]] = None,
            max_rows_number: int = 5,
            start_row: int = 0,
            scroll_step: int = 1,
            initial_text: str = None
    ) -> None:

        self.messages = {}
        self.user_language = user_language
        self.kb_language = kb_language
        if initial_text is None:
            self._text = translate_context("en", self.user_language, "You forgot to change initial text")
        else:
            self._text = translate_context(self.kb_language, self.user_language, initial_text)
        scroll_keys = self.create_buttons_list(scroll_buttons)
        top_static_buttons = self.create_buttons_list(top_buttons)
        bottom_static_buttons = self.create_buttons_list(bottom_buttons)

        super().__init__(scroll_keys, top_static_buttons, bottom_static_buttons,
                         max_rows_number, start_row, scroll_step, user_language)
        if scroll_keys:
            self.KEY_UP.text = translate_context("en", self.user_language, self.KEY_UP.text)
            self.KEY_DOWN.text = translate_context("en", self.user_language, self.KEY_DOWN.text)

    def create_buttons_list(self, dict_list: List[List[dict]]) -> List[List[InlineKeyboardButton]]:
        """Функція приймає dict_list:List[List[dict]] та повертає об'єкт списку списків з інлайн клавіатурами типу
        List[List[InlineKeyboardButton]], що необхідно для подальшого формування клавіатури.
        При створенні клавіатури створюється словник даних self.messages, що відповідає за повідомлення при натисканні
        кнопок. Кнопки та повідомлення перекладаються на необхідну мову self.user_language"""
        if dict_list is None:
            return []
        buttons_list = []
        for item in dict_list:
            if isinstance(item, list):
                buttons_list.append(self.create_buttons_list(item))
            elif isinstance(item, dict):
                callback_data = item["callback_data"]
                text = translate_context(self.kb_language, self.user_language, item["text"])
                message = translate_context(self.kb_language, self.user_language, item["message"])
                buttons_list.append(InlineKeyboardButton(text=text, callback_data=callback_data))
                self.messages[callback_data] = message
        return buttons_list

    @property
    def text(self):
        """Повертає self._text"""
        return self._text

    @text.setter
    def text(self, value):
        """Змінює або задає self._text"""
        self._text = value

    def callback(self, event: CallbackQuery):
        """Змінює self._text при виклику колбеку"""
        self._text = self.messages[event.data]


class MyKeyboard(ContextInlineKeyboardGenerator):
    """Клас клавіатури як приклад використання ContextInlineKeyboardGenerator.
    Списки кнопок визначаються всередині класу."""
    def __init__(
            self,
            user_language: str,
            max_rows_number: int = 5,
            start_row: int = 0,
            scroll_step: int = 1,
    ):
        self.name = "Приклад клавіатури"

        kb_language = "uk"
        top_buttons = [
            [
                {"callback_data": "button_1",
                 "text": "Кнопка 1",
                 "message": "Ти натиснув кнопку 1"},
                {"callback_data": "button_2",
                 "text": "Кнопка 2",
                 "message": "Ти натиснув кнопку 2"}
            ],
            [
                {"callback_data": "button_3",
                 "text": "Кнопка 3",
                 "message": "Ти натиснув кнопку 3"}
            ]
        ]

        scroll_buttons = None
        bottom_buttons = [
            [
                {"callback_data": "button_4",
                 "text": "Кнопка 4",
                 "message": "Ти натиснув кнопку 4"}
            ]
        ]

        initial_text = "Привіт, це твоє початкове тестове повідомлення"

        super().__init__(user_language, kb_language, top_buttons, scroll_buttons, bottom_buttons,
                         max_rows_number, start_row, scroll_step, initial_text)


class MyContextUserKeyboard(CombineInlineKeyboardGenerator):
    """Клас, що описує конкретну клавіатуру користувача.
    В даному класі описуються функції, що повертають параметри обробки колбеку для кожної кнопки."""

    def __init__(
            self,
            max_rows_number: int = 5,
            start_row: int = 0,
            scroll_step: int = 1,
            user_language: str = 'en'
    ) -> None:
        self.user_language = user_language if user_language in supported_languages else "en"
        self.scroll_keys = self.language_context_buttons(context_button_set["scroll_key_buttons"],
                                                         context_button_set_languages)
        self.top_static_buttons = self.language_context_buttons(context_button_set["top_static_buttons"],
                                                                context_button_set_languages)
        self.bottom_static_buttons = self.language_context_buttons(context_button_set["bottom_static_buttons"],
                                                                   context_button_set_languages)
        self.max_rows_number = max_rows_number
        self.start_row = start_row
        self.scroll_step = scroll_step

    def context_callback_message(self, event: CallbackQuery) -> str:
        if event.data == "scroll_up":
            return f"{self.language_context_text('scroll_up', default_buttons_messages)}"
        elif event.data == "scroll_down":
            return f"{self.language_context_text('scroll_down', default_buttons_messages)}"
        elif event.data.startswith("inline_button_"):
            return f"{self.language_context_text('inline_button_', context_callback_messages)}" \
                   f"{event.data.lstrip('inline_button_')}"
        elif event.data.startswith("top_button_"):
            return f"{self.language_context_text('top_button_', context_callback_messages)}" \
                   f"{event.data.lstrip('top_button_')}"
        elif event.data.startswith("bottom_button_"):
            return f"{self.language_context_text('bottom_button_', context_callback_messages)}" \
                   f"{event.data.lstrip('bottom_button_')}"
