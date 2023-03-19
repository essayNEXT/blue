from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from utils.storages import TmpStorage


from settings import BOT_TOKEN


storage = MemoryStorage()
tmp_storage = TmpStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=storage, tmp_storage=tmp_storage)
