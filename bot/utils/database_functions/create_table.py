from .connection import con
from psycopg2 import OperationalError


def execut_query(query, connection=con):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print('Query executed successfully')
    except OperationalError as e:
        print(f'Error{e}')


create_message_table = """
CREATE TABLE IF NOT EXISTS message(
message TEXT,
userid INTEGER,
message_time TIMESTAMP)"""

execut_query(create_message_table)
