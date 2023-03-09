from aiogram import Router
from aiogram.types import Message
from utils.database_functions.create_table import execut_query

router = Router()


@router.message()
async def echo(message: Message):
    insert_query = (f"INSERT INTO message (message, userid) "
                    f"VALUES ({message.text},{message.from_user.id})")
    execut_query(insert_query)

    await message.answer(message.text)
