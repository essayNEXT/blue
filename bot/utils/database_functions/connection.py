from psycopg2 import OperationalError, connect
import os

name = os.environ['POSTGRES_DB']
user = os.environ['POSTGRES_USER']
password = os.environ['POSTGRES_PASSWORD']
host = os.environ['DB_HOST']
port = os.environ['DB_PORT']
a = os.environ.get('')

def create_connection(
        db_name=name,
        db_user=user,
        db_password=password,
        db_host=host,
        db_port=port
):
    try:
        connection = connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print('Connection to DB successfull')
        print(db_name, db_port, db_host, db_password, db_user)
    except OperationalError as e:
        print(f'Error connecting {e}')
        print(db_name, db_port, db_host, db_password, db_user)
        connection = None
    return connection


con = create_connection()
