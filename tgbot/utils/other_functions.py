# - *- coding: utf- 8 - *-
from tgbot.services.sqlite import get_user
from aiogram.types import Message, CallbackQuery
from tgbot.utils.translations import get_text, get_user_language, format_number
from tgbot.services.sqlite import update_settings
from tgbot.utils.utils_functions import get_admins, get_unix
from tgbot.data.loader import bot

def convert_ref(ref):
    ref = int(ref)
    refs = ['реферал', 'реферала', 'рефералов']

    if ref % 10 == 1 and ref % 100 != 11:
        count = 0
    elif 2 <= ref % 10 <= 4 and (ref % 100 < 10 or ref % 100 >= 20):
        count = 1
    else:
        count = 2

    return f"{refs[count]}"

def open_profile(user_id):
    user = get_user(id=user_id)
    lang = get_user_language(user_id)
    
    return get_text(lang, 'profile_text',
                   user_name=user['user_name'],
                   user_id=user['id'],
                   balance=format_number(user['balance']),
                   total_refill=format_number(user['total_refill']),
                   reg_date=user['reg_date'],
                   ref_count=user['ref_count'])


# Автоматическая очистка ежедневной статистики после 00:00
async def update_profit_day():

    update_settings(profit_day=get_unix())


# Автоматическая очистка еженедельной статистики в понедельник 00:00
async def update_profit_week():
    update_settings(profit_week=get_unix())

async def autobackup_db():
    db_path = "tgbot/data/database.db"
    with open(db_path, "rb") as data:
        for admin in get_admins():
            await bot.send_document(chat_id=admin, document=data, caption="<b>⚙️ АвтоБэкап базы данных ⚙️</b>")