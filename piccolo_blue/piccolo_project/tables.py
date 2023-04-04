from piccolo.table import Table
from piccolo.columns.column_types import Text, Integer


class Users(Table, tablename="users"):
    name = Text()
    number_phone = Integer()


class Languages(Table, tablename='languages'):
    language = Text()
    abbr_language = Text()
