# file for testing translation functions

from ttranslator.google import *

txt = "Доброго дня. Як справи?"
print(txt)

print(LangDetect(txt))             # detecting text language
print(LangGet('en'))               # display the name and code of the language
print(gTranslate(txt, "en"))       # display translation of a text string into the specified language, or an error message
