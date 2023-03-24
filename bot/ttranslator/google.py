# googletrans==3.1.0a0
from googletrans import *
from pathlib import Path
import csv

# Write to dictionary <LangDict> information about language and code from <google_languages.csv>
lang_file = Path(Path.cwd(), 'ttranslator', 'google_languages.csv')
with open(lang_file, 'r') as f:
    reader = csv.DictReader(f)
    LangDict = {'language': 'code'}
    for row in reader:
        LangDict.update({row['language']: row['code']})

# -------------------------------------------------------------
def LangDetect(text, s='all'):
    # Detect text language;
    #    s = 'lang' - return code;
    #    s = 'confidence' - return confidence;
     if s == 'lang':
         return Translator().detect(text).lang
     if s == 'confidence':
         return Translator().detect(text).confidence
     return Translator().detect(text)


def LangGet(lang: str = 'en') -> dict:
    # returns the name and code of the language
    for key, value in LangDict.items():
        if key == lang or value == lang:
            return {key: value}
    return {lang: 'incorrect'}

def LangCheck(lang: str = 'language') -> bool:
    # Is there a language name or code in the language table?
    for key, value in LangDict.items():
        if key == lang or value == lang:
            return True
    return False

def gTranslate(input_text: str = 'Text translation', lang: str = 'en') -> str:
    # Translation of a text string into the specified language, or an error message
    if LangCheck(lang):
        try:
            tr = Translator().translate(input_text, scr='en', dest=lang)
            return tr.text
        except:
            return "Error"
    return 'language is missing in the table!'

# ---------------------------------------------------------------------------------------------------------------------
# Technical function for testing
# lang_test() - Prints to the console a list of all languages and their codes from the dictionary
# lang_test('code') - tries to make a translation for all codes from the dictionary
# lang_test('lang') - tries to make a translation for all language names from the dictionary
# lang_test(language, text) - Translation of a text string into the language, if it is possible

def lang_test(lang='0', input_text='Завтра ми уезжаем в Польшу'):
    if lang == '0':
        count_of_lang = 0
        print("Output all values:")
        for key, value in LangDict.items():
            print(key, value)
            count_of_lang += 1
        print(f"count: {count_of_lang}")
        return 0

    if lang == "code":
        print("Testing by code")
        for key, value in LangDict.items():
            try:
                tr = Translator().translate(input_text, dest=value)
                print((key + " " + value).ljust(30, " "), "Ok")
            except:
                print((key + " " + value).ljust(30, " "), "!!! Error !!!")
        return 0

    if lang == "lang":
        print("Testing by code")
        for key, value in LangDict.items():
            try:
                tr = Translator().translate(input_text, dest=key)
                print((key + " " + value).ljust(30, " "), "Ok")
            except:
                print((key + " " + value).ljust(30, " "), "!!! Error !!!")
        return 0

    print(LangGet(lang))
    print(input_text)
    print(LangDetect(input_text))
    print(gTranslate(input_text, lang))