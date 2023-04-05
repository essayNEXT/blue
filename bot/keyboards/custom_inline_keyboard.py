from typing import List, Dict
from .inline import AbstractInlineKeyboard, ContextInlineKeyboardGenerator
from aiogram.types import CallbackQuery
from utils.translate.kb_translate import translate_context


class MyCustomKeyboard(AbstractInlineKeyboard):
    """Приклад використання абстрактного класу створення клавіатури AbstractInlineKeyboard."""

    def define_initial_text(self) -> str:
        initial_text = "Hello, this is your initial test message"
        return initial_text

    def define_kb_language(self) -> str:
        kb_language = "en"
        return kb_language

    def define_callback_pattern(self) -> str:
        callback_pattern = "#_test_"
        return callback_pattern

    def define_top_buttons(self) -> List[List[Dict[str, str]]]:
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

    def define_scroll_buttons(self) -> List[List[Dict[str, str]]]:
        scroll_buttons = [
            [
                {"callback_data": f"#_test_button_scroll_{num}",
                 "text": f"Scroll button {num}",
                 "message": f"You pressed scroll button {num}"}] for num in range(1, 8)
        ]
        return scroll_buttons

    def define_bottom_buttons(self) -> List[List[Dict[str, str]]]:
        bottom_buttons = [
            [
                {"callback_data": "#_test_button_4",
                 "text": "Button 4",
                 "message": "You pressed bottom button 4"}
            ]
        ]
        return bottom_buttons

    def callback(self, event: CallbackQuery) -> None:
        self.text = translate_context(self.kb_language, self.user_language, "You press button")


class MyKeyboard(ContextInlineKeyboardGenerator):
    """Клас клавіатури як приклад використання ContextInlineKeyboardGenerator.
    Списки кнопок визначаються всередині класу.
    Обов'язкові параметри класу:
        - kb_language - мова клавіатури за замовчуванням
        - callback_pattern - шаблон колбеку (префікс) класу клавіатури
        - initial_text - початковий текст класу клавіатури @property
        - top_buttons - список списків словників верхніх кнопок клавіатури
        - scroll_buttons - список списків словників кнопок прокручування клавіатури
        - bottom_buttons - список списків словників нижніх кнопок клавіатури
    Далі виконуємо ініціацію батьківського класу ContextInlineKeyboardGenerator.
    super().__init__(user_language, kb_language, callback_pattern, top_buttons, scroll_buttons, bottom_buttons,
                    initial_text, max_rows_number, start_row, scroll_step).
    При необхідності можна перевизначити метод callback для обробки колбеків від користувачів.
    """

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
