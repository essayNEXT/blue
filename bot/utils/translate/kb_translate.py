from googletrans import Translator
from typing import List

# Імітація бази даних перекладу клавіатури
translation = {
    "uk": {
        "You forgot to change initial text": "Ти забув змінити параметр початкового тексту"
    },
    "en": {"<class 'keyboards.custom_inline_keyboard.MyCustomKeyboard>'": {
        "initial_text": "Hello, this is your initial test message",
        "top_buttons": [
            [
                {"callback_data": "#_test_button_1",
                 "text": "Button 1",
                 "message": "You pressed the top button 1"},
                {"callback_data": "#_test_button_2",
                 "text": "Button 2",
                 "message": "You pressed the top button 2"}
            ],
            [
                {"callback_data": "#_test_button_3",
                 "text": "Button 3",
                 "message": "You pressed the top button 3"}
            ]
        ],
        "bottom_buttons": [
            [
                {"callback_data": "#_test_button_4",
                 "text": "Button 4",
                 "message": "You pressed the bottom button 4"}
            ]
        ],
        "scroll_buttons": [
            [
                {"callback_data": f"#_test_button_scroll_{num}",
                 "text": f"Scroll button {num}",
                 "message": f"You pressed the scroll button {num}"}
            ] for num in range(1, 8)
        ]
    }},
    "ru": {
        "button_2": "Кнопка 2"
    }
}

# Імітація бази даних одиничних перекладів рядків
single_translation = {
    "uk": {},
    "en": {},
    "ru": {}
}


def translate_context(
        src_lng: str = None,
        trg_lan: str = None,
        context_text: str = None,
        self_object=None,
        context_data: dict = None
):
    """
    Функція перекладу контексту. Приймає два варіанти вхідних даних:
    1. Переклад тексту:
        - src_lng: str - мова об'єкту, що перекладається
        - trg_lan: str - цільова мова перекладу
        - context_text: str - текст, що необхідно перекласти
    2. Переклад контекстних даних екземпляру клавіатури:
        - self_object - екземпляр класу клавіатури
        - context_data: dict - словник з даними для перекладу, що містить в собі:
            "initial_text" - початковий текст при виклику клавіатури
            "top_buttons" - список списків верхніх кнопок
            "scroll_buttons" - список списків кнопок прокручування
            "bottom_buttons" - список списків нижніх кнопок
    Повертає відповідні об'єкти в залежності від варіанту введених вхідних даних.
    """

    def translate_buttons_list(target_lan: str, buttons_list: List[List[dict]]) -> List[List[dict]]:
        """Функція перекладу списку списків словників кнопок клавіатури"""
        if buttons_list is None:
            return []
        new_list = []
        for item in buttons_list:
            if isinstance(item, list):
                new_list.append(translate_buttons_list(target_lan, item))
            elif isinstance(item, dict):
                item["text"] = google_translate(target_lan, item["text"])
                if "message" in item.keys():
                    item["message"] = google_translate(target_lan, item["message"])
                new_list.append(item)
        return new_list

    try:
        if context_text and context_data:
            raise KeyError("Input data is not correct!")

        # Варіант 1
        elif context_text:
            if src_lng == trg_lan:
                print(f"{context_text} - is in keyboard object")
                return context_text
            else:
                if trg_lan in single_translation.keys() and context_text in single_translation[trg_lan].keys():
                    print(f"{context_text} - is get from db")
                    return single_translation[trg_lan][context_text]
                else:
                    print(f"{context_text} - is get from Google translate")
                    text = google_translate(trg_lan, context_text)

                    # імітація занесення перекладу до БД single_translation
                    if trg_lan not in single_translation.keys():
                        single_translation[trg_lan] = {}
                    single_translation[trg_lan][context_text] = text
                    return text

        # Варіант 2
        elif self_object and context_data:
            src_lng = self_object.kb_language
            trg_lan = self_object.user_language

            if src_lng == trg_lan:
                return context_data

            # Перевіряємо наявність перекладу context_data для класу клавіатури в базі даних
            if trg_lan in translation.keys() and str(self_object.__class__) in translation[trg_lan].keys():
                print("Context_data - get from db")
                return translation[trg_lan][str(self_object.__class__)]  # повинні отримати з БД
            # Якщо в базі даних переклад відсутній, то виконуємо переклад поелементно
            else:
                print(f"Google translate every single element of context_data from {src_lng} to {trg_lan}")
                context_data["initial_text"] = google_translate(trg_lan, context_data["initial_text"])
                context_data["top_buttons"] = translate_buttons_list(trg_lan, context_data["top_buttons"])
                context_data["scroll_buttons"] = translate_buttons_list(trg_lan, context_data["scroll_buttons"])
                context_data["bottom_buttons"] = translate_buttons_list(trg_lan, context_data["bottom_buttons"])

                # імітуємо занесення перекладу клавіатур на мову користувача дл бази даних
                if trg_lan not in translation.keys():
                    translation[trg_lan] = {}
                translation[trg_lan][str(self_object.__class__)] = context_data

                return context_data

        else:
            return None
    except KeyError as e:
        print(f"Error {e}")


def google_translate(trg_lan: str, input_text: str) -> str:
    """Функція перекладу тексту за допомогою перекладача гугл.
    Приймає:
        - trg_lan: str - цільова мова перекладу
        - input_text: str - текст для перекладу
    Повертає рядок з перекладеним текстом"""
    tr = Translator().translate(input_text, dest=trg_lan)
    return tr.text
