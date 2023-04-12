from piccolo.table import Table
from piccolo.columns.column_types import Text, Integer, JSON


class Users(Table, tablename="users"):
    name = Text()
    number_phone = Integer()


class Languages(Table, tablename='languages'):
    language = Text()
    abbr_language = Text()


class Translate_file(Table, tablename='translate_object'):
    language = Text()
    abbr_language = Text()
    json_kb = JSON()

