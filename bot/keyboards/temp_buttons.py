from typing import List
from aiogram.types import InlineKeyboardButton

top_button_1 = {"name": "top_button_1",
                "text": {"en": "top button 1",
                         "uk": "верхня кнопка 1"},
                "callback_data": "top_button_1",
                "message_text": {"en": "Push button 1",
                                 "uk": "Натиснув кнопку 1"}
                }
top_button_2 = {"name": "top_button_2",
                "text": {"en": "top button 2",
                         "uk": "верхня кнопка 2"},
                "callback_data": "top_button_2",
                "message_text": {"en": "Push button 2",
                                 "uk": "Натиснув кнопку 2"}
                }

temp_top_static_buttons = {
    1: [top_button_1],
    2: [top_button_2]
}

scroll_button_1 = {"name": "scroll_button_1",
                   "text": {"en": "scroll button 1",
                            "uk": "верхня кнопка 1"},
                   "callback_data": "scroll_button_1",
                   "message_text": {"en": "Push scroll button 1",
                                    "uk": "Натиснув скрол кнопку 1"}
                   }

scroll_button_2 = {"name": "scroll_button_2",
                   "text": {"en": "scroll button 2",
                            "uk": "верхня кнопка 2"},
                   "callback_data": "scroll_button_2",
                   "message_text": {"en": "Push scroll button 2",
                                    "uk": "Натиснув скрол кнопку 2"}
                   }

scroll_button_3 = {"name": "scroll_button_3",
                   "text": {"en": "scroll button 3",
                            "uk": "верхня кнопка 3"},
                   "callback_data": "scroll_button_3",
                   "message_text": {"en": "Push scroll button 3",
                                    "uk": "Натиснув скрол кнопку 3"}
                   }

scroll_button_4 = {"name": "scroll_button_4",
                   "text": {"en": "scroll button 4",
                            "uk": "верхня кнопка 4"},
                   "callback_data": "scroll_button_4",
                   "message_text": {"en": "Push scroll button 4",
                                    "uk": "Натиснув скрол кнопку 4"}
                   }

scroll_button_5 = {"name": "scroll_button_5",
                   "text": {"en": "scroll button 5",
                            "uk": "верхня кнопка 5"},
                   "callback_data": "scroll_button_5",
                   "message_text": {"en": "Push scroll button 5",
                                    "uk": "Натиснув скрол кнопку 5"}
                   }

scroll_button_6 = {"name": "scroll_button_6",
                   "text": {"en": "scroll button 6",
                            "uk": "верхня кнопка 6"},
                   "callback_data": "scroll_button_6",
                   "message_text": {"en": "Push scroll button 6",
                                    "uk": "Натиснув скрол кнопку 6"}
                   }

temp_scroll_keys = {
    1: [scroll_button_1],
    2: [scroll_button_2],
    3: [scroll_button_3],
    4: [scroll_button_4],
    5: [scroll_button_5],
    6: [scroll_button_6],
}

bottom_button_1 = {"name": "bottom_button_1",
                   "text": {"en": "bottom button 1",
                            "uk": "нижня кнопка 1"},
                   "callback_data": "bottom_button_1",
                   "message_text": {"en": "Push button 1",
                                    "uk": "Натиснув нижню кнопку 1"}
                   }
bottom_button_2 = {"name": "bottom_button_2",
                   "text": {"en": "bottom button 2",
                            "uk": "нижня кнопка 2"},
                   "callback_data": "bottom_button_2",
                   "message_text": {"en": "Push button 2",
                                    "uk": "Натиснув нижню кнопку 2"}
                   }

bottom_button_3 = {"name": "bottom_button_3",
                   "text": {"en": "bottom button 3",
                            "uk": "нижня кнопка 3"},
                   "callback_data": "bottom_button_3",
                   "message_text": {"en": "Push button 3",
                                    "uk": "Натиснув нижню кнопку 3"}
                   }

temp_bottom_static_buttons = {
    1: [bottom_button_1],
    2: [bottom_button_2, bottom_button_3],
}


def get_inline_buttons_list(button_dict: dict, user_language: str) -> List[List[InlineKeyboardButton]]:
    result = []
    for level in range(1, len(button_dict) + 1):
        buttons_in_level = []
        for single_button in button_dict[level]:
            button = InlineKeyboardButton(text=single_button['text'][user_language],
                                          callback_data=single_button["callback_data"])
            buttons_in_level.append(button)
        result.append(buttons_in_level)
    return result

button = InlineKeyboardButton(text="text", callback_data="callback_data")
button.text = "hello"
print(button.json())