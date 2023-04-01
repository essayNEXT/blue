from googletrans import Translator

translation = {
    "uk": {
        "You forgot to change initial text": "Ти забув змінити параметр початкового тексту"
    },
    "en": {"<class 'keyboards.inline.MyKeyboard'>": {
        "Кнопка 1": "Button 1",
        "Кнопка 2": "Button 2",
        "Кнопка 3": "Button 3",
        "Кнопка 4": "Button 4",
        "Ти натиснув кнопку 1": "You push to button 1",
        "Ти натиснув кнопку 2": "You push to button 2",
        "Ти натиснув кнопку 3": "You push to button 3",
        "Ти натиснув кнопку 4": "You push to button 4",
        "Привіт, це твоє початкове тестове повідомлення": "Hello, it is your initial message"
    }},
    "ru": {
        "button_2": "Кнопка 2"
    }
}


def translate_context(src_lng: str = None, trg_lan: str = None, context_text: str = None,
                      self_object=None, context_data=None):
    if self_object and context_data:
        print("Клас всередині translate_context - ", self_object.__class__)
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


def google_translate(out_language: str, input_text: str) -> str:
    tr = Translator().translate(input_text, dest=out_language)
    return tr.text
