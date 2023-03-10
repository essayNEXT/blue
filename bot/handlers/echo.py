from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from utils.database_functions.create_table import execut_query
from datetime import datetime

router = Router()


@router.message(Command('read_last'))
async def cmd_read_last(message: Message):
    insert_query = "SELECT message_time FROM message ORDER BY message_time DESC LIMIT 1"
    val = execut_query(insert_query)
    print(insert_query)
    await message.answer(f'Дата последнего сообщения  в БД {val}')


@router.message()
async def echo(message: Message):
    date = datetime.now().isoformat(" ")
    insert_query = (f"INSERT INTO message (message, userid, message_time) "
                    f"VALUES ('{message.text}','{message.from_user.id}','{date}')")
    execut_query(insert_query)

    await message.answer(message.text)
