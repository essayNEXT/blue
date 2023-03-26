from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from redis.asyncio.client import Redis
import os

from utils.storages import TmpStorage
from aiogram.fsm.storage.redis import RedisStorage

from settings import BOT_TOKEN

redis = Redis(
        port=os.environ.get('REDIS_PORT'),
        host=os.environ.get('REDIS_HOST')
    )

tmp_storage = TmpStorage()
storage = RedisStorage(redis=redis)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=storage, tmp_storage=tmp_storage)

