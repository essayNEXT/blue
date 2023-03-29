from aiogram.types import InlineKeyboardButton

context_button_set_languages = {
    "inline_button_1": {"uk": "Скрол кнопка 1",
                        "ru": "Скролл кнопка 1"},
    "inline_button_2": {"uk": "Скрол кнопка 2",
                        "ru": "Скролл кнопка 2"},
    "inline_button_3": {"uk": "Скрол кнопка 3",
                        "ru": "Скролл кнопка 3"},
    "inline_button_4": {"uk": "Скрол кнопка 4",
                        "ru": "Скролл кнопка 4"},
    "inline_button_5": {"uk": "Скрол кнопка 5",
                        "ru": "Скролл кнопка 5"},
    "inline_button_6": {"uk": "Скрол кнопка 6",
                        "ru": "Скролл кнопка 6"},
    "inline_button_7": {"uk": "Скрол кнопка 7",
                        "ru": "Скролл кнопка 7"},
    "inline_button_8": {"uk": "Скрол кнопка 8",
                        "ru": "Скролл кнопка 8"},
    "inline_button_9": {"uk": "Скрол кнопка 9",
                        "ru": "Скролл кнопка 9"},
    "inline_button_10": {"uk": "Скрол кнопка 10",
                         "ru": "Скролл кнопка 10"},
    "bottom_button_1": {"uk": "Нижня кнопка 1",
                        "ru": "Нижняя кнопка 1"},
    "bottom_button_2": {"uk": "Нижня кнопка 2",
                        "ru": "Нижняя кнопка 2"},
    "bottom_button_3": {"uk": "Нижня кнопка 3",
                        "ru": "Нижняя кнопка 3"},
    "top_button_1": {"uk": "Верхня кнопка 1",
                     "ru": "Верхняя кнопка 1"},
}

num_of_scrolls = 10

scroll_key_buttons = [
    [
        InlineKeyboardButton(
            text=f"Inline button {button}",
            callback_data=f"inline_button_{button}"
        )
    ] for button in range(1, num_of_scrolls + 1)
]

top_static_buttons = [
    [
        InlineKeyboardButton(
            text="Top button 1",
            callback_data="top_button_1"
        ),
    ],
]

bottom_static_buttons = [
    [
        InlineKeyboardButton(
            text="Bottom button 1",
            callback_data="bottom_button_1"
        ),
    ],
    [
        InlineKeyboardButton(
            text="Bottom button 2",
            callback_data="bottom_button_2"
        ),
        InlineKeyboardButton(
            text="Bottom button 3",
            callback_data="bottom_button_3"
        ),
    ]
]

context_button_set = {"scroll_key_buttons": scroll_key_buttons,
                      "top_static_buttons": top_static_buttons,
                      "bottom_static_buttons": bottom_static_buttons}

context_callback_messages = {
    "inline_button_": {"en": "After press to scroll inline button ",
                       "uk": "Після натискання на скрол кнопку ",
                       "ru": "После нажатия на скролл кнопкy "},
    "bottom_button_": {"en": "After press to bottom button ",
                       "uk": "Після натискання на нижню кнопку ",
                       "ru": "После нажатия на нижнюю кнопкy "},
    "top_button_": {"en": "After press to top button ",
                    "uk": "Після натискання на верхню кнопку ",
                    "ru": "После нажатия на верхнюю кнопкy "},
}

default_buttons_messages = {
    "scroll_up": {"en": "After button up",
                  "uk": "Після натискання на кнопку вверх",
                  "ru": "После нажатия на кнопкy вверх"},
    "scroll_down": {"en": "After button down",
                    "uk": "Після натискання на кнопку вниз",
                    "ru": "После нажатия на кнопкy вниз"},
    "exit": {"en": "After press to exit button ",
             "uk": "Після натискання на кнопку вийти",
             "ru": "После нажатия на кнопкy выйти"}
}

navigation_buttons = {
    "scroll_up": {"en": "Up",
                  "uk": "Вверх",
                  "ru": "Вверх"},
    "scroll_down": {"en": "Down",
                    "uk": "Вниз",
                    "ru": "Вниз"}
}
