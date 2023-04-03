from itertools import chain
from typing import List, Optional
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from dataclasses import dataclass
from aiogram.types import CallbackQuery
# from enum import Enum
from utils.translate.kb_translate import translate_context


# class Language(Enum):
#     ukrainian = "uk"
#     russian = "ru"
#     english = "en"


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
    ) -> None:

        self.scroll_keys = scroll_keys
        self.max_rows_number = max_rows_number
        self.start_row = start_row
        self.scroll_step = scroll_step

        self.up_key = self.KEY_UP.copy()
        self.down_key = self.KEY_DOWN.copy()

    def _get_current_scroll_keyboard_list(self) -> List[List[InlineKeyboardButton]]:
        """Повертає поточний список скролінгової клавіатури"""
        self.numbers_of_buttons_to_show = self.max_rows_number
        current_scroll_keyboard: List[List[InlineKeyboardButton]] = []
        if self.start_row != 0:
            current_scroll_keyboard = [[self.up_key]] + current_scroll_keyboard
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
                    + [[self.down_key]]
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
    ) -> None:
        super().__init__(scroll_keys, max_rows_number, start_row, scroll_step)
        if not top_static_buttons:
            top_static_buttons = []
        self.top_static_buttons = top_static_buttons
        if not bottom_static_buttons:
            bottom_static_buttons = []
        self.bottom_static_buttons = bottom_static_buttons

    def markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=list(chain(self.top_static_buttons,
                                       self._get_current_scroll_keyboard_list(),
                                       self.bottom_static_buttons))
        )


class ContextInlineKeyboardGenerator(CombineInlineKeyboardGenerator):
    """Клас-шаблон для створення клавіатури.
    Приймає обов'язкові параметри:
        - user_language: str - мова користувача
        - kb_language: str - мова на якій створений клас клавіатури
        - callback_pattern: str - шаблон колбеку класу клавіатури
    Приймає необов'язкові параметри:
        - top_buttons: Optional[List[List[dict]]] - список словників верхніх кнопок
        - scroll_buttons: Optional[List[List[dict]]] - список словників скрол кнопок
        - bottom_buttons: Optional[List[List[dict]]] - список словників нижніх кнопок
        - initial_text: str - початковий текст при виклику клавіатури
        - max_rows_number: int - максимальна кількість об'єктів прокручування
        - start_row: int - початковий рядок прокручування
        - scroll_step: int - крок прокручування
        """

    def __init__(
            self,
            user_language: str,
            kb_language: str,
            callback_pattern: str,
            top_buttons: Optional[List[List[dict]]] = None,
            scroll_buttons: Optional[List[List[dict]]] = None,
            bottom_buttons: Optional[List[List[dict]]] = None,
            initial_text: str = None,
            max_rows_number: int = 5,
            start_row: int = 0,
            scroll_step: int = 1,
    ) -> None:

        self.messages = {}
        self.user_language = user_language
        self.kb_language = kb_language
        self.callback_pattern = callback_pattern

        data_for_translate = {
            "initial_text": initial_text,
            "top_buttons": top_buttons,
            "scroll_buttons": scroll_buttons,
            "bottom_buttons": bottom_buttons
        }
        self.translated_data = translate_context(self_object=self, context_data=data_for_translate)

        if initial_text is None:
            self._text = translate_context("en", self.user_language, "You forgot to change initial text")
        else:
            self._text = self.translated_data["initial_text"]

        scroll_keys = self.create_buttons_list(self.translated_data["scroll_buttons"])
        top_static_buttons = self.create_buttons_list(self.translated_data["top_buttons"])
        bottom_static_buttons = self.create_buttons_list(self.translated_data["bottom_buttons"])

        super().__init__(
            scroll_keys, top_static_buttons, bottom_static_buttons,
            max_rows_number, start_row, scroll_step)

        print("Клас всередині ContextInlineKeyboardGenerator - ", self.__class__)
        if scroll_keys:
            self.up_key.text = translate_context("en", self.user_language, self.KEY_UP.text)
            self.up_key.callback_data = self.callback_pattern + self.KEY_UP.callback_data
            self.down_key.text = translate_context("en", self.user_language, self.KEY_DOWN.text)
            self.down_key.callback_data = self.callback_pattern + self.KEY_DOWN.callback_data

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
                text = item["text"]
                if "message" in item.keys():
                    message = item["message"]
                    self.messages[callback_data] = message
                buttons_list.append(InlineKeyboardButton(text=text, callback_data=callback_data))
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
        """Функція обробки колбеків. За необхідності можна перевизначити в похідному класі.
        За замовчуванням замінює параметр self._text на повідомлення при натисканні кнопки."""
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

        kb_language = "uk"
        callback_pattern = "#_test_"
        initial_text = "Привіт, це твоє початкове тестове повідомлення"

        top_buttons = [
            [
                {"callback_data": "#_test_button_1",
                 "text": "Кнопка 1",
                 "message": "Ти натиснув верхню кнопку 1"},
                {"callback_data": "#_test_button_2",
                 "text": "Кнопка 2",
                 "message": "Ти натиснув верхню кнопку 2"}
            ],
            [
                {"callback_data": "#_test_button_3",
                 "text": "Кнопка 3",
                 "message": "Ти натиснув верхню кнопку 3"}
            ]
        ]

        scroll_buttons = [
            [
                {"callback_data": f"#_test_button_scroll_{num}",
                 "text": f"Кнопка прокручування {num}",
                 "message": f"Ти натиснув кнопку прокручування {num}"}
            ] for num in range(1, 8)
        ]

        bottom_buttons = [
            [
                {"callback_data": "#_test_button_4",
                 "text": "Кнопка 4",
                 "message": "Ти натиснув нижню кнопку 4"}
            ]
        ]

        super().__init__(user_language, kb_language, callback_pattern, top_buttons, scroll_buttons, bottom_buttons,
                         initial_text, max_rows_number, start_row, scroll_step)
        print("Клас всередині MyKeyboard - ", self.__class__)
