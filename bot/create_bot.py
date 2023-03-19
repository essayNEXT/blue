from aiogram import Bot, Dispatcher
from utils.storages import TmpStorage

from settings import BOT_TOKEN

tmp_storage = TmpStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(tmp_storage=tmp_storage)
