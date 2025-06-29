# - *- coding: utf- 8 - *-
import asyncio

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from tgbot.services.sqlite import get_payments, update_payments
from tgbot.utils.utils_functions import ots
from tgbot.keyboards.inline_admin import payments_settings_info, payments_settings, payments_back
from tgbot.filters.is_admin import IsAdmin
from tgbot.data import config
from tgbot.utils.translations import get_text

# Создаём роутер для этого модуля
router = Router()

# Константы для платежных систем
qiwi_text = "🥝 QIWI"
yoomoney_text = "💳 ЮMoney"
lava_text = "🌋 LavaPay"
lzt_text = "⚡ LolzTeam"
crystalPay_text = "💎 Crystal Pay"

@router.callback_query(IsAdmin(), F.data == 'payments')
async def payments_settings_choose(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text("<b>⚙️ Выберите способ оплаты</b>", reply_markup=payments_settings())

@router.callback_query(IsAdmin(), F.data.startswith("payments:"))
async def payments_info(call: CallbackQuery, state: FSMContext):
    await state.clear()
    way = call.data.split(":")[1]

    def pay_info(way, status):
        if status == "True":
            status = "✅ Включен"
        elif status == "False":
            status = "❌ Выключен"

        msg = f"""
<b>{way}

Статус: <code>{status}</code></b>        
"""
        return ots(msg)

    if way == "qiwi":
        ways = qiwi_text
        status = get_payments()['pay_qiwi']
        await call.message.edit_text(pay_info(ways, status), reply_markup=payments_settings_info(way, status))
    elif way == "yoomoney":
        ways = yoomoney_text
        status = get_payments()['pay_yoomoney']
        await call.message.edit_text(pay_info(ways, status), reply_markup=payments_settings_info(way, status))
    elif way == "lava":
        ways = lava_text
        status = get_payments()['pay_lava']
        await call.message.edit_text(pay_info(ways, status), reply_markup=payments_settings_info(way, status))
    elif way == "lzt":
        ways = lzt_text
        status = get_payments()['pay_lolz']
        await call.message.edit_text(pay_info(ways, status), reply_markup=payments_settings_info(way, status))
    elif way == "crystalPay":
        ways = crystalPay_text
        status = get_payments()['pay_crystal']
        await call.message.edit_text(pay_info(ways, status), reply_markup=payments_settings_info(way, status))

@router.callback_query(IsAdmin(), F.data.startswith("payments_on_off:"))
async def off_payments(call: CallbackQuery, state: FSMContext):
    way = call.data.split(":")[1]
    action = call.data.split(":")[2]

    def pay_info(way, status):
        if status == "True":
            status = "✅ Включен"
        elif status == "False":
            status = "❌ Выключен"

        msg = f"""
<b>{way}

Статус: <code>{status}</code></b>        
"""
        return ots(msg)

    if way == "qiwi":
        ways = qiwi_text
        if action == "off":
            update_payments(pay_qiwi="False")
        else:
            update_payments(pay_qiwi="True")
        status = get_payments()['pay_qiwi']
        await call.message.edit_text(pay_info(ways, status), reply_markup=payments_settings_info(way, status))
    elif way == "yoomoney":
        ways = yoomoney_text
        if action == "off":
            update_payments(pay_yoomoney="False")
        else:
            update_payments(pay_yoomoney="True")
        status = get_payments()['pay_yoomoney']
        await call.message.edit_text(pay_info(ways, status), reply_markup=payments_settings_info(way, status))
    elif way == "lava":
        ways = lava_text
        if action == "off":
            update_payments(pay_lava="False")
        else:
            update_payments(pay_lava="True")
        status = get_payments()['pay_lava']
        await call.message.edit_text(pay_info(ways, status), reply_markup=payments_settings_info(way, status))
    elif way == "lzt":
        ways = lzt_text
        if action == "off":
            update_payments(pay_lolz="False")
        else:
            update_payments(pay_lolz="True")
        status = get_payments()['pay_lolz']
        await call.message.edit_text(pay_info(ways, status), reply_markup=payments_settings_info(way, status))
    elif way == "crystalPay":
        ways = crystalPay_text
        if action == "off":
            update_payments(pay_crystal="False")
        else:
            update_payments(pay_crystal="True")
        status = get_payments()['pay_crystal']
        await call.message.edit_text(pay_info(ways, status), reply_markup=payments_settings_info(way, status))

@router.callback_query(IsAdmin(), F.data.startswith("payments_balance:"))
async def payments_balance_call(call: CallbackQuery, state: FSMContext):
    await state.clear()
    way = call.data.split(":")[1]

    if way == "qiwi":
        ways = qiwi_text
        try:
            # Здесь нужно будет импортировать и использовать Qiwi класс
            # qiwi = Qiwi(config.qiwi_token, config.qiwi_login, config.qiwi_secret)
            # balance = await qiwi.get_balance(config.qiwi_login)
            balance = "Проверка баланса QIWI временно недоступна"
            await call.message.edit_text(f"{ways} \n\n{balance}", reply_markup=payments_back())
        except Exception as e:
            await call.message.edit_text(f"{ways} \n\nОшибка при получении баланса: {str(e)}", reply_markup=payments_back())

    elif way == "yoomoney":
        ways = yoomoney_text
        try:
            # Здесь нужно будет импортировать и использовать YooMoney класс
            # yoo = YooMoney(config.yoomoney_token, config.yoomoney_number)
            # balance = yoo.get_balance()
            balance = "Проверка баланса ЮMoney временно недоступна"
            await call.message.edit_text(f"{ways} \n\n<code>{balance}</code>", reply_markup=payments_back())
        except Exception as e:
            await call.message.edit_text(f"{ways} \n\nОшибка при получении баланса: {str(e)}", reply_markup=payments_back())

    elif way == "crystalPay":
        ways = crystalPay_text
        try:
            # Здесь нужно будет импортировать и использовать CrystalPay класс
            # crystal = CrystalPay(config.crystal_Cassa, config.crystal_Token)
            # balance = await crystal.get_balance()
            balance = "Проверка баланса CrystalPay временно недоступна"
            await call.message.edit_text(f"{ways} \n\n{balance}", reply_markup=payments_back())
        except Exception as e:
            await call.message.edit_text(f"{ways} \n\nОшибка при получении баланса: {str(e)}", reply_markup=payments_back())

    elif way == "lzt":
        ways = lzt_text
        try:
            # Здесь нужно будет импортировать и использовать Lolz класс
            # lzt = Lolz(config.lolz_token)
            # await asyncio.sleep(3)
            # data = await lzt.get_user()
            # balance = data['balance']
            # hold = data['hold']
            balance = "Проверка баланса LolzTeam временно недоступна"
            await call.message.edit_text(f'{ways} \n\n{balance}', reply_markup=payments_back())
        except Exception as e:
            await call.message.edit_text(f'{ways} \n\nОшибка при получении баланса: {str(e)}', reply_markup=payments_back())

    elif way == "lava":
        ways = lava_text
        try:
            # Здесь нужно будет импортировать и использовать Lava класс
            # lava = Lava(config.lava_project_id, config.lava_secret_key)
            # balance = await lava.get_balance()
            balance = "Проверка баланса LavaPay временно недоступна"
            await call.message.edit_text(f"{ways} \n\n{balance}", reply_markup=payments_back())
        except Exception as e:
            await call.message.edit_text(f"{ways} \n\nОшибка при получении баланса: {str(e)}", reply_markup=payments_back())

@router.callback_query(IsAdmin(), F.data.startswith("payments_info:"))
async def payments_info_open(call: CallbackQuery, state: FSMContext):
    await state.clear()
    way = call.data.split(":")[1]

    if way == "qiwi":
        ways = qiwi_text
        qiwi_login = getattr(config, 'qiwi_login', 'Не настроен')
        qiwi_token = getattr(config, 'qiwi_token', 'Не настроен')
        qiwi_secret = getattr(config, 'qiwi_secret', 'Не настроен')
        await call.message.edit_text(f"{ways} \n\nНомер: <code>{qiwi_login}</code> \nТокен: <code>{qiwi_token}</code> \nСекретный p2p-ключ: <code>{qiwi_secret}</code>", reply_markup=payments_back())

    elif way == "crystalPay":
        ways = crystalPay_text
        crystal_cassa = getattr(config, 'crystal_Cassa', 'Не настроен')
        crystal_token = getattr(config, 'crystal_Token', 'Не настроен')
        await call.message.edit_text(f"{ways} \n\nЛогин кассы: <code>{crystal_cassa}</code> \nСекретный токен 1: <code>{crystal_token}</code>", reply_markup=payments_back())

    elif way == "yoomoney":
        ways = yoomoney_text
        yoomoney_token = getattr(config, 'yoomoney_token', 'Не настроен')
        yoomoney_number = getattr(config, 'yoomoney_number', 'Не настроен')
        await call.message.edit_text(f"{ways} \n\nТокен: <code>{yoomoney_token}</code> \nНомер: <code>{yoomoney_number}</code>", reply_markup=payments_back())
    
    elif way == "lzt":
        ways = lzt_text
        lolz_token = getattr(config, 'lolz_token', 'Не настроен')
        lolz_nick = getattr(config, 'lolz_nick', 'Не настроен')
        lolz_id = getattr(config, 'lolz_id', 'Не настроен')
        await call.message.edit_text(f"{ways} \n\nТокен: <code>{lolz_token}</code> \nНик: <code>{lolz_nick}</code> \nID: <code>{lolz_id}</code>", reply_markup=payments_back())
    
    elif way == "lava":
        ways = lava_text
        lava_project_id = getattr(config, 'lava_project_id', 'Не настроен')
        lava_secret_key = getattr(config, 'lava_secret_key', 'Не настроен')
        await call.message.edit_text(f"{ways} \n\nID Проекта: <code>{lava_project_id}</code> \nСекретный ключ: <code>{lava_secret_key}</code>", reply_markup=payments_back()) 