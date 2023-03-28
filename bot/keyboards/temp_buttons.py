from typing import List
from aiogram.types import InlineKeyboardButton

# top_button_1 = {"name": "top_button_1",
#                 "text": {"en": "top button 1",
#                          "uk": "верхня кнопка 1"},
#                 "callback_data": "top_button_1",
#                 "message_text": {"en": "Push button 1",
#                                  "uk": "Натиснув кнопку 1"}
#                 }
# top_button_2 = {"name": "top_button_2",
#                 "text": {"en": "top button 2",
#                          "uk": "верхня кнопка 2"},
#                 "callback_data": "top_button_2",
#                 "message_text": {"en": "Push button 2",
#                                  "uk": "Натиснув кнопку 2"}
#                 }
#
# temp_top_static_buttons = {
#     1: [top_button_1],
#     2: [top_button_2]
# }


# def get_inline_buttons_list(button_dict: dict, user_language: str) -> List[List[InlineKeyboardButton]]:
#     result = []
#     for level in range(1, len(button_dict) + 1):
#         buttons_in_level = []
#         for single_button in button_dict[level]:
#             button = InlineKeyboardButton(text=single_button['text'][user_language],
#                                           callback_data=single_button["callback_data"])
#             buttons_in_level.append(button)
#         result.append(buttons_in_level)
#     return result

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


# def get_inline_buttons_list(
#         button_list: List[List[InlineKeyboardButton]],
#         user_language: str
# ) -> List[List[InlineKeyboardButton]]:
#     new_buttons_list = []
#     for raw in button_list:
#         buttons_in_raw = []
#         for single_button in raw:
#             single_button.text = context_button_set_languages[single_button.callback_data][user_language]
#             buttons_in_raw.append(single_button)
#         new_buttons_list.append(buttons_in_raw)
#     return new_buttons_list

