from .inline import KeyboardOfDict, ContextInlineKeyboardGenerator
from utils.translate.kb_translate import translate_context
from aiogram.types import CallbackQuery


class MyCustomKeyboard(ContextInlineKeyboardGenerator):
    """Приклад використання абстрактного класу створення клавіатури AbstractInlineKeyboard."""

    @property
    def initial_text(self) -> str:
        initial_text = "Hello, it is your test keyboard № 1"
        return initial_text

    @property
    def kb_language(self) -> str:
        kb_language = "en"
        return kb_language

    @property
    def callback_pattern(self) -> str:
        callback_pattern = "#_test_"
        return callback_pattern

    @property
    def max_rows_number(self) -> int:
        return 5

    @property
    def translate_function(self):
        return translate_context

    @property
    def top_buttons(self) -> KeyboardOfDict:
        top_buttons = [
            [
                {"callback_data": "#_test_button_1",
                 "text": "Button 1",
                 "message": "You pressed top button 1"},
                {"callback_data": "#_test_button_2",
                 "text": "Button 2",
                 "message": "You pressed top button 2"}
            ],
            [
                {"callback_data": "#_test_button_3",
                 "text": "Button 3",
                 "message": "You pressed top button 3"}
            ]
        ]
        return top_buttons

    @property
    def scroll_buttons(self) -> KeyboardOfDict:
        scroll_buttons = [
            [
                {"callback_data": f"#_test_button_scroll_{num}",
                 "text": f"Scroll button {num}",
                 "message": f"You pressed scroll button {num}"}] for num in range(1, 20)
        ]
        return scroll_buttons

    @property
    def bottom_buttons(self) -> KeyboardOfDict:
        bottom_buttons = [
            [
                {"callback_data": "#_test_button_4",
                 "text": "Button 4",
                 "message": "You pressed bottom button 4"}
            ]
        ]
        return bottom_buttons

    def callback(self, event: CallbackQuery) -> None:
        """
        Функція обробки колбеків. За необхідності можна перевизначити в похідному класі.
        За замовчуванням замінює параметр self._text на повідомлення при натисканні кнопки.
        """
        self._text = self.messages[event.data]


class MyCustomKeyboard2(ContextInlineKeyboardGenerator):
    """Приклад використання абстрактного класу створення клавіатури AbstractInlineKeyboard."""

    @property
    def initial_text(self) -> str:
        initial_text = "Привіт, це тестова клавіатура № 2"
        return initial_text

    @property
    def kb_language(self) -> str:
        kb_language = "uk"
        return kb_language

    @property
    def callback_pattern(self) -> str:
        callback_pattern = "#_test2_"
        return callback_pattern

    @property
    def max_rows_number(self) -> int:
        return 3

    @property
    def translate_function(self):
        return translate_context

    @property
    def top_buttons(self) -> KeyboardOfDict | None:
        top_buttons = None
        return top_buttons

    @property
    def scroll_buttons(self) -> KeyboardOfDict:
        scroll_buttons = [
            [
                {"callback_data": f"#_test2_button_scroll_{num}",
                 "text": f"Кнопка прокручування {num}",
                 "message": f"Ти натиснув кнопку прокручування {num}"}] for num in range(1, 7)
        ]
        return scroll_buttons

    @property
    def bottom_buttons(self) -> KeyboardOfDict:
        bottom_buttons = [
            [
                {"callback_data": "#_test2_button_done",
                 "text": "DONE",
                 "message": "Ти підтвердив, що мав підтвердити"}
            ]
        ]
        return bottom_buttons

    def callback(self, event: CallbackQuery) -> None:
        """
        Функція обробки колбеків. За необхідності можна перевизначити в похідному класі.
        За замовчуванням замінює параметр self._text на повідомлення при натисканні кнопки.
        """
        self._text = self.messages[event.data]
