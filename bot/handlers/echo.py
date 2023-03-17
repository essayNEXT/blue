from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from utils.database_functions.execute_query import execute_query
from datetime import datetime
from utils.database_functions.connection import con

router = Router()


@router.message(Command('read_last'))
async def cmd_read_last(message: Message):
    cursor = con.cursor()
    cursor.execute("SELECT message FROM message ORDER BY message_time DESC LIMIT 1")
    val = cursor.fetchone()
    await message.answer(f'Останнє повідомлення в БД "{val[0]}"')


@router.message()
async def echo(message: Message):
    date = datetime.now().isoformat(" ")
    insert_query = (f"INSERT INTO message (message, userid, message_time) "
                    f"VALUES ('{message.text}','{message.from_user.id}','{date}')")
    execute_query(insert_query)

    await message.answer(message.text)
