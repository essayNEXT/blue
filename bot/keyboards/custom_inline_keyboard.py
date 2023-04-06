from .inline import AbstractInlineKeyboard, KeyboardOfDict
from aiogram.types import CallbackQuery
# from utils.translate.kb_translate import translate_context


class MyCustomKeyboard(AbstractInlineKeyboard):
    """Приклад використання абстрактного класу створення клавіатури AbstractInlineKeyboard."""

    def define_initial_text(self) -> str:
        initial_text = "Hello, this is your initial test message"
        return initial_text

    @property
    def kb_language(self) -> str:
        kb_language = "en"
        return kb_language

    @property
    def callback_pattern(self) -> str:
        callback_pattern = "#_test_"
        return callback_pattern

    def define_top_buttons(self) -> KeyboardOfDict:
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

    def define_scroll_buttons(self) -> KeyboardOfDict:
        scroll_buttons = [
            [
                {"callback_data": f"#_test_button_scroll_{num}",
                 "text": f"Scroll button {num}",
                 "message": f"You pressed scroll button {num}"}] for num in range(1, 8)
        ]
        return scroll_buttons

    def define_bottom_buttons(self) -> KeyboardOfDict:
        bottom_buttons = [
            [
                {"callback_data": "#_test_button_4",
                 "text": "Button 4",
                 "message": "You pressed bottom button 4"}
            ]
        ]
        return bottom_buttons

    def callback(self, event: CallbackQuery) -> None:
        super(MyCustomKeyboard, self).callback(event)
