from aiogram import Router
from aiogram.types import Message
from utils.database_functions.create_table import execut_query
from datetime import datetime

router = Router()


@router.message()
async def echo(message: Message):
    date = datetime.now().isoformat(" ")
    insert_query = (f"INSERT INTO message (message, userid, message_time) "
                    f"VALUES ('{message.text}','{message.from_user.id}','{date}')")
    execut_query(insert_query)

    await message.answer(message.text)
