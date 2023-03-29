import os
from aiogram import Bot, Dispatcher
from utils.storages import TmpStorage
# from redis.asyncio.client import Redis
# from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.memory import MemoryStorage
from settings import BOT_TOKEN

# redis = Redis(
#
#         port=os.environ.get('REDIS_PORT'),
#         host=os.environ.get('REDIS_HOST')
#     )
#
# storage = RedisStorage(redis=redis)
storage = MemoryStorage()
tmp_storage = TmpStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=storage, tmp_storage=tmp_storage)
