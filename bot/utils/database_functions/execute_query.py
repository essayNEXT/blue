from .connection import con
from psycopg2 import OperationalError


def execute_query(query, connection=con):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print('Query executed successfully')
    except OperationalError as e:
        print(f'Error{e}')
