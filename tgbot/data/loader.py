# - *- coding: utf- 8 - *-
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from tgbot.data.config import bot_token

# Создаем бота с новым синтаксисом aiogram 3.x
bot = Bot(
    token=bot_token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

# Создаем диспетчер с хранилищем
dp = Dispatcher(storage=MemoryStorage())

# Планировщик задач
scheduler = AsyncIOScheduler()