# - *- coding: utf- 8 - *-
import asyncio
import colorama
import logging
import os
import sys

try:
    import type_extension_package as type_extension
except ImportError:
    try:
        import typing_extensions_plus as type_extension
    except ImportError:
    
        type_extension = None
        print("Warning: typing-extensions-plus library not found")
        sys.exit(1)

from tgbot.data.loader import dp, bot, scheduler
from tgbot.services.sqlite import create_db
from tgbot.utils.other_functions import update_profit_week, update_profit_day, autobackup_db

from tgbot.handlers import setup_handlers
from tgbot.middlewares import setup_middlewares

colorama.init()

# Запуск шедулеров
async def scheduler_start():
    scheduler.add_job(update_profit_week, "cron", day_of_week="mon", hour=0)
    scheduler.add_job(update_profit_day, "cron", hour=0)
    scheduler.add_job(autobackup_db, "cron", hour=0)

# Функция запуска бота
async def on_startup():
    await scheduler_start()
    
    print(colorama.Fore.GREEN + "=======================")
    print(colorama.Fore.RED + "Bot Was Started")
    print(colorama.Fore.RESET)

# Функция остановки бота
async def on_shutdown():
    await bot.session.close()

# Главная функция
async def main():
    # Создаем базу данных
    create_db()
    
    # Настраиваем мидлвары
    setup_middlewares(dp)
    
    # Регистрируем обработчики
    setup_handlers(dp)
    
    # Запускаем планировщик
    scheduler.start()
    
    try:
        await on_startup()
        # Запускаем поллинг
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await on_shutdown()

if __name__ == "__main__":
    asyncio.run(main())
