import asyncio
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from Config_bot import bot_token

storage = MemoryStorage()

loop = asyncio.get_event_loop()
bot = Bot(bot_token, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage, loop=loop)
