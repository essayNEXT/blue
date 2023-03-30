from googletrans import Translator

translation = {
    "uk": {
        "You forgot to change initial text": "Ти забув змінити параметр початкового тексту"
    },
    "en": {
        "Кнопка 1": "Button 1",
        "Кнопка 2": "Button 2",
        "Кнопка 3": "Button 3",
        "Кнопка 4": "Button 4",
        "Ти натиснув кнопку 1": "You push to button 1",
        "Ти натиснув кнопку 2": "You push to button 2",
        "Ти натиснув кнопку 3": "You push to button 3",
        "Ти натиснув кнопку 4": "You push to button 4",
        "Привіт, це твоє початкове тестове повідомлення": "Hello, it is your initial message"
    },
    "ru": {
        "button_2": "Кнопка 2"
    }
}


def translate_context(init_language, out_language, context_data):
    if init_language == out_language:
        print(f"{context_data} - is in keyboard object")
        return context_data
    else:
        if out_language in translation.keys() and context_data in translation[out_language].keys():
            print(f"{context_data} - is get from db")
            return translation[out_language][context_data]
        else:
            print(f"{context_data} - is get from Google translate")
            text = google_translate(out_language, context_data)
            return text


def google_translate(out_language: str, input_text: str) -> str:
    tr = Translator().translate(input_text, dest=out_language)
    return tr.text
