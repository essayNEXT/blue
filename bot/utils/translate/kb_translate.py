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
        return context_data
    else:
        if context_data in translation[out_language].keys():
            print("Get data from db")
            return translation[out_language][context_data]
        else:
            print("need to use google translate")
            return context_data
            # return google_translate(init_language, out_language, context_data)


def google_translate(init_language: str, out_language: str, input_text: str) -> str:
    # Translation of a text string into the specified language, or an error message
    tr = Translator().translate(input_text, scr=out_language, dest=init_language)
    return tr.text
