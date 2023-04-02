from googletrans import Translator


# Імітація бази даних
translation = {
    "uk": {
        "You forgot to change initial text": "Ти забув змінити параметр початкового тексту"
    },
    "en": {"<class 'keyboards.inline.MyKeyboard'>": {
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
                 "text": f"Scroll utton {num}",
                 "message": f"You pressed the scroll button {num}"}
            ] for num in range(1, 8)
        ]
    }},
    "ru": {
        "button_2": "Кнопка 2"
    }
}


def translate_context(
        src_lng: str = None,
        trg_lan: str = None,
        context_text: str = None,
        self_object=None,
        context_data: dict = None
):
    """Функція перекладу контексту. Приймає два варіанти вхідних даних:
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
    # Варіант 2
    if self_object and context_data:
        src_lng = self_object.kb_language
        trg_lan = self_object.user_language

        if src_lng == trg_lan:
            return context_data

        # Перевіряємо наявність перекладу context_data для класу клавіатури в базі даних
        if trg_lan in translation.keys() and str(self_object.__class__) in translation[trg_lan].keys():
            print("Context_data get from DB")
            return translation[trg_lan][str(self_object.__class__)]  # повинні отримати з БД
        # Якщо в базі даних переклад відсутній, то виконуємо переклад поелементно
        else:
            print(f"Google translate every single element from {src_lng} to {trg_lan}")
    # Варіант 1
    elif context_text:
        if src_lng == trg_lan:
            print(f"{context_text} - is in keyboard object")
            return context_text
        else:
            if trg_lan in translation.keys() and context_data in translation[trg_lan].keys():
                print(f"{context_text} - is get from db")
                return translation[trg_lan][context_text]
            else:
                print(f"{context_text} - is get from Google translate")
                text = google_translate(trg_lan, context_text)
                return text
    else:
        return None


def google_translate(out_language: str, input_text: str) -> str:
    tr = Translator().translate(input_text, dest=out_language)
    return tr.text
