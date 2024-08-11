from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN


storage = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=storage)
