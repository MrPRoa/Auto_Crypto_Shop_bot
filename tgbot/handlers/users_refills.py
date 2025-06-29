# - *- coding: utf- 8 - *-
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
import aiohttp
import asyncio
from datetime import datetime, timedelta
import time
import random
import logging

from tgbot.services.sqlite import get_user, update_user_balance_and_refill, get_payments, get_settings, add_refill, add_used_transaction_db, is_transaction_used_db
from tgbot.keyboards.inline_user import refill_inl, user_menu, back_to_user_menu, refill_open_inl, crypto_refill_inl, crypto_refill_polygon_inl, cancel_refill_inl, crypto_refill_waiting_inl, crypto_refill_erc20_inl
from tgbot.utils.translations import get_text, get_user_language
from tgbot.data import config
from tgbot.services.crypto_usdt import CryptoUSDT
from tgbot.utils.crypto_validation import validate_private_key_for_network, validate_all_crypto_keys

# Создаём роутер для этого модуля
router = Router()

# Хранилище для отслеживания времени создания платежей
payment_times = {}

# Хранилище для отслеживания использованных транзакций
used_transactions = set()

def add_used_transaction(tx_hash):
    """Добавляем хеш транзакции в список использованных"""
    used_transactions.add(tx_hash)

def is_transaction_used(tx_hash):
    """Проверяем, была ли транзакция уже использована"""
    return tx_hash in used_transactions

class RefillStates(StatesGroup):
    waiting_amount = State()
    waiting_payment = State()

@router.callback_query(F.data == "refill")
async def refill_menu(call: CallbackQuery, state: FSMContext):
    """Главное меню пополнений"""
    await state.clear()
    user_id = call.from_user.id
    lang = get_user_language(user_id)
    
    # Проверяем включены ли пополнения
    settings = get_settings()
    if not settings or settings.get('is_refill') != "True":
        await call.answer(get_text(lang, 'refill_disabled'), show_alert=True)
        return
        
    text = get_text(lang, 'choose_payment')
    await call.message.edit_text(text, reply_markup=refill_inl())

@router.callback_query(F.data.startswith("refill:"))
async def process_refill_method(call: CallbackQuery, state: FSMContext):
    """Обработка выбора метода пополнения"""
    user_id = call.from_user.id
    lang = get_user_language(user_id)
    
    method = call.data.split(":")[1]
    
    # Сохраняем выбранный метод
    await state.update_data(refill_method=method)
    await state.set_state(RefillStates.waiting_amount)
    
    text = get_text(lang, 'enter_amount', min_amount=1, max_amount=10000)
    await call.message.edit_text(text, reply_markup=cancel_refill_inl(user_id))

@router.message(RefillStates.waiting_amount)
async def process_refill_amount(message: Message, state: FSMContext):
    """Обработка суммы пополнения"""
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    
    try:
        amount = float(message.text.replace(',', '.'))
        if amount < 1:
            await message.answer("❌ Минимальная сумма пополнения: $1")
            return
        if amount > 10000:
            await message.answer("❌ Максимальная сумма пополнения: $10,000")
            return
            
        # Получаем данные из состояния
        data = await state.get_data()
        method = data.get('refill_method')
        
        # В зависимости от метода создаем платеж
        if method == "yoomoney":
            await process_yoomoney_payment(message, state, amount)
        elif method == "lava":
            await process_lava_payment(message, state, amount)
        elif method == "crystal":
            await process_crystal_payment(message, state, amount)
        elif method == "lolz":
            await process_lolz_payment(message, state, amount)
        elif method == "crypto_usdt":
            await process_crypto_payment(message, state, amount)
        elif method == "crypto_usdt_polygon":
            await process_crypto_polygon_payment(message, state, amount)
        elif method == "crypto_usdt_erc20":
            await process_crypto_erc20_payment(message, state, amount)
        else:
            await message.answer("❌ Неизвестный метод оплаты", reply_markup=user_menu(user_id))
            await state.clear()
            
    except (ValueError, AttributeError):
        text = get_text(lang, 'amount_must_be_number')
        await message.answer(text)

async def process_yoomoney_payment(message: Message, state: FSMContext, amount: float):
    """Обработка пополнения через ЮMoney"""
    user_id = message.from_user.id
    
    # Конвертируем доллары в рубли (примерный курс)
    rub_amount = round(amount * 95, 2)  # Примерный курс $1 = 95₽
    payment_id = f"yoomoney_{user_id}_{int(amount)}"
    
    text = f"""💰 Пополнение через ЮMoney

💰 Сумма: ${amount} (≈{rub_amount}₽)
🔗 Нажмите кнопку "Оплатить" для перехода к оплате

⏰ После оплаты нажмите "Проверить платеж"
"""
    
    await message.answer(text, reply_markup=refill_open_inl("yoomoney", amount, f"https://yoomoney.ru/quickpay/confirm.xml?receiver=4100118188797772&quickpay-form=shop&targets=Пополнение&paymentType=SB&sum={rub_amount}", payment_id))
    await state.clear()

async def process_lava_payment(message: Message, state: FSMContext, amount: float):
    """Обработка пополнения через Lava"""
    user_id = message.from_user.id
    
    payment_id = f"lava_{user_id}_{int(amount)}"
    
    text = f"""🌋 Пополнение через LavaPay

💰 Сумма: ${amount}
🔗 Нажмите кнопку "Оплатить" для перехода к оплате

⏰ После оплаты нажмите "Проверить платеж"
"""
    
    await message.answer(text, reply_markup=refill_open_inl("lava", amount, f"https://lava.ru/payment/{amount}", payment_id))
    await state.clear()

async def process_crystal_payment(message: Message, state: FSMContext, amount: float):
    """Обработка пополнения через CrystalPay"""
    user_id = message.from_user.id
    
    payment_id = f"crystal_{user_id}_{int(amount)}"
    
    text = f"""🥝 Пополнение через CrystalPay

💰 Сумма: ${amount}
🔗 Нажмите кнопку "Оплатить" для перехода к оплате

⏰ После оплаты нажмите "Проверить платеж"
"""
    
    await message.answer(text, reply_markup=refill_open_inl("crystal", amount, f"https://crystal-pay.com/payment/{amount}", payment_id))
    await state.clear()

async def process_lolz_payment(message: Message, state: FSMContext, amount: float):
    """Обработка пополнения через LolzTeam"""
    user_id = message.from_user.id
    
    payment_id = f"lolz_{user_id}_{int(amount)}"
    
    text = f"""⚡ Пополнение через LolzTeam

💰 Сумма: ${amount}
🔗 Нажмите кнопку "Оплатить" для перехода к оплате

⏰ После оплаты нажмите "Проверить платеж"
"""
    
    await message.answer(text, reply_markup=refill_open_inl("lolz", amount, f"https://lolz.guru/market/balance/add/{amount}", payment_id))
    await state.clear()

async def process_crypto_payment(message: Message, state: FSMContext, amount: float):
    """Обработка пополнения через USDT"""
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    
    print(f"\n💰 CRYPTO CREATE: Создание криптоплатежа для пользователя {user_id}")
    print(f"💰 Запрошенная сумма: ${amount}")
    
    # Базовая проверка конфигурации
    if not hasattr(config, 'crypto_wallet_address') or not config.crypto_wallet_address or not hasattr(config, 'bscscan_api_key') or not config.bscscan_api_key or not hasattr(config, 'polygonscan_api_key') or not config.polygonscan_api_key or not hasattr(config, 'etherscan_api_key') or not config.etherscan_api_key or not hasattr(config, 'crypto_private_key') or not config.crypto_private_key:
        print(f"❌ CRYPTO CREATE: Криптоплатежи не настроены")
        await message.answer("❌ Криптоплатежи временно недоступны")
        await state.clear()
        return
    
    # Проверка валидности приватного ключа для BSC сети
    key_validation = validate_private_key_for_network(config.crypto_private_key, 'bsc')
    if not key_validation['valid']:
        print(f"❌ CRYPTO CREATE: {key_validation['error']}")
        await message.answer(get_text(lang, 'crypto_config_error'))
        await state.clear()
        return
    
    # Генерируем уникальный ID платежа
    payment_id = f"crypto_{user_id}_{int(time.time())}"
    
    # Генерируем сумму с копейками для идентификации
    crypto_service = CryptoUSDT(config.crypto_wallet_address, config.crypto_private_key, config.bscscan_api_key, config.polygonscan_api_key, config.etherscan_api_key)
    exact_amount = crypto_service.generate_payment_amount(amount)
    
    # Сохраняем время создания платежа
    payment_times[payment_id] = datetime.now()
    print(f"💾 CRYPTO CREATE: Сохранено время платежа {payment_id}: {payment_times[payment_id]}")
    
    # Текст с инструкциями
    crypto_text = f"""💰 Пополнение через USDT BEP-20

💰 Сумма к пополнению: <code>{exact_amount}</code>
📍 Адрес кошелька:
<code>{config.crypto_wallet_address}</code>

⚠️ ВАЖНО! Переведите точно <code>{exact_amount}</code> USDT в сети BEP-20
💡 Дополнительные копейки нужны для автоматической идентификации вашего платежа

⏰ Время на перевод: 1 час
💰 На баланс зачислится полная сумма пополнения с копейками
🔄 После перевода нажмите "Проверить платеж"

Платеж автоматически отменится через 1 час"""
    
    await message.answer(crypto_text, reply_markup=crypto_refill_inl(exact_amount, payment_id), parse_mode="HTML")
    await state.clear()

async def process_crypto_polygon_payment(message: Message, state: FSMContext, amount: float):
    """Обработка пополнения через USDT в сети Polygon"""
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    
    print(f"\n💰 CRYPTO POLYGON CREATE: Создание криптоплатежа Polygon для пользователя {user_id}")
    print(f"💰 Запрошенная сумма: ${amount}")
    
    # Базовая проверка конфигурации
    if not hasattr(config, 'crypto_wallet_address') or not config.crypto_wallet_address or not hasattr(config, 'bscscan_api_key') or not config.bscscan_api_key or not hasattr(config, 'polygonscan_api_key') or not config.polygonscan_api_key or not hasattr(config, 'etherscan_api_key') or not config.etherscan_api_key or not hasattr(config, 'crypto_private_key') or not config.crypto_private_key:
        print(f"❌ CRYPTO POLYGON CREATE: Криптоплатежи не настроены")
        await message.answer(get_text(lang, 'crypto_unavailable'))
        await state.clear()
        return
    
    # Проверка валидности приватного ключа для Polygon сети
    key_validation = validate_private_key_for_network(config.crypto_private_key, 'polygon')
    if not key_validation['valid']:
        print(f"❌ CRYPTO POLYGON CREATE: {key_validation['error']}")
        await message.answer(get_text(lang, 'crypto_config_error'))
        await state.clear()
        return
    
    # Генерируем уникальный ID платежа
    payment_id = f"crypto_polygon_{user_id}_{int(time.time())}"
    
    # Генерируем сумму с копейками для идентификации
    crypto_service = CryptoUSDT(config.crypto_wallet_address, "", config.bscscan_api_key, config.polygonscan_api_key)
    exact_amount = crypto_service.generate_payment_amount(amount)
    
    # Сохраняем время создания платежа
    payment_times[payment_id] = datetime.now()
    print(f"💾 CRYPTO POLYGON CREATE: Сохранено время платежа {payment_id}: {payment_times[payment_id]}")
    
    # Текст с инструкциями
    crypto_text = f"""💰 Пополнение через USDT Polygon

💰 Сумма к пополнению: <code>{exact_amount}</code>
📍 Адрес кошелька:
<code>{config.crypto_wallet_address}</code>

⚠️ ВАЖНО! Переведите точно <code>{exact_amount}</code> USDT в сети Polygon
💡 Дополнительные копейки нужны для автоматической идентификации вашего платежа

⏰ Время на перевод: 1 час
💰 На баланс зачислится полная сумма пополнения с копейками
🔄 После перевода нажмите "Проверить платеж"

Платеж автоматически отменится через 1 час"""
    
    await message.answer(crypto_text, reply_markup=crypto_refill_polygon_inl(exact_amount, payment_id), parse_mode="HTML")
    await state.clear()

@router.callback_query(F.data.startswith("check_opl:"))
async def check_payment(call: CallbackQuery):
    """Проверка обычных платежей (не крипто)"""
    user_id = call.from_user.id
    lang = get_user_language(user_id)
    
    await call.answer(get_text(lang, 'payment_check'), show_alert=True)

async def check_usdt_transaction(wallet_address, amount, api_key, payment_time, time_limit_hours=1):
    """Проверка USDT транзакции через BSCScan API"""
    try:
        if not wallet_address or not api_key:
            print(f"❌ CRYPTO DEBUG: Отсутствуют необходимые параметры")
            return {'found': False, 'error': 'Configuration error'}
        
        # USDT контракт на BSC
        usdt_contract = "0x55d398326f99059ff775485246999027b3197955"
        
        payment_timestamp = int(payment_time.timestamp())
        start_time = payment_timestamp - 600  # 10 минут буфер
        end_time = payment_timestamp + (time_limit_hours * 3600)
        current_time = int(time.time())
        
        print(f"\n🔍 CRYPTO DEBUG: Проверка USDT транзакции")
        print(f"💰 Ожидаемая сумма: ${amount}")
        print(f"💳 Кошелек: {wallet_address}")
        
        if current_time > end_time:
            print(f"❌ CRYPTO DEBUG: Время платежа истекло")
            return {'found': False, 'error': 'Payment time expired'}
        
        url = f"https://api.bscscan.com/api"
        params = {
            'module': 'account',
            'action': 'tokentx',
            'contractaddress': usdt_contract,
            'address': wallet_address,
            'startblock': 0,
            'endblock': 999999999,
            'sort': 'desc',
            'apikey': api_key
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                print(f"📡 BSCScan статус: {response.status}")
                
                if response.status == 200:
                    data = await response.json()
                    
                    if data['status'] == '1' and data['result']:
                        transactions = data['result']
                        print(f"📋 Найдено {len(transactions)} транзакций")
                        
                        for i, tx in enumerate(transactions):
                            if i >= 10:  # Проверяем только первые 10
                                break
                                
                            if tx['to'].lower() == wallet_address.lower():
                                tx_time = int(tx['timeStamp'])
                                if start_time <= tx_time <= end_time:
                                    if is_transaction_used_db(tx['hash']):
                                        continue
                                    
                                    tx_amount = float(tx['value']) / (10**18)
                                    
                                    if abs(tx_amount - amount) < 0.001:
                                        print(f"✅ НАЙДЕНА ТРАНЗАКЦИЯ: {tx['hash']}")
                                        return {
                                            'found': True,
                                            'hash': tx['hash'],
                                            'amount': tx_amount,
                                            'from': tx['from'],
                                            'timestamp': tx_time
                                        }
                    
                    return {'found': False, 'error': None}
                else:
                    return {'found': False, 'error': f'BSCScan API error: {response.status}'}
                    
    except Exception as e:
        print(f"💥 CRYPTO DEBUG: Ошибка: {str(e)}")
        return {'found': False, 'error': str(e)}

async def check_usdt_transaction_polygon(wallet_address, amount, api_key, payment_time, time_limit_hours=1):
    """Проверка транзакций USDT в сети Polygon через Polygonscan API"""
    try:
        print(f"🔍 POLYGON CHECK: Проверяем транзакции для {wallet_address}")
        print(f"💰 Ожидаемая сумма: {amount} USDT")
        
        start_time = int(payment_time.timestamp()) - 300  # 5 минут до создания платежа
        end_time = int(time.time()) + 300  # 5 минут после текущего времени
        
        url = "https://api.polygonscan.com/api"
        params = {
            'module': 'account',
            'action': 'tokentx',
            'contractaddress': '0xc2132D05D31c914a87C6611C10748AEb04B58e8F',  # USDT Polygon contract
            'address': wallet_address,
            'page': 1,
            'offset': 100,
            'startblock': 0,
            'endblock': 99999999,
            'sort': 'desc',
            'apikey': api_key
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                print(f"📡 POLYGON API: Статус ответа: {response.status}")
                
                if response.status == 200:
                    data = await response.json()
                    
                    if data['status'] == '1' and data['result']:
                        transactions = data['result']
                        print(f"📋 POLYGON: Найдено {len(transactions)} транзакций")
                        
                        for i, tx in enumerate(transactions):
                            if i >= 10:  # Проверяем только первые 10
                                break
                                
                            if tx['to'].lower() == wallet_address.lower():
                                tx_time = int(tx['timeStamp'])
                                if start_time <= tx_time <= end_time:
                                    if is_transaction_used_db(tx['hash']):
                                        continue
                                    
                                    tx_amount = float(tx['value']) / (10**18)
                                    
                                    if abs(tx_amount - amount) < 0.001:
                                        print(f"✅ POLYGON: НАЙДЕНА ТРАНЗАКЦИЯ: {tx['hash']}")
                                        return {
                                            'found': True,
                                            'hash': tx['hash'],
                                            'amount': tx_amount,
                                            'from': tx['from'],
                                            'timestamp': tx_time
                                        }
                    
                    return {'found': False, 'error': None}
                else:
                    return {'found': False, 'error': f'Polygonscan API error: {response.status}'}
                    
    except Exception as e:
        print(f"💥 POLYGON DEBUG: Ошибка: {str(e)}")
        return {'found': False, 'error': str(e)}

@router.callback_query(F.data.startswith("check_crypto:"))
async def check_crypto_payment(call: CallbackQuery):
    """Проверка криптоплатежа"""
    user_id = call.from_user.id
    
    data = call.data.split(":")
    amount = float(data[1])
    payment_id = data[2]
    
    print(f"\n🚀 CRYPTO CHECK: Пользователь {user_id} проверяет платеж ${amount}")
    
    if payment_id not in payment_times:
        await call.message.edit_text(
            "❌ Данные о платеже не найдены. Создайте новый платеж.",
            reply_markup=user_menu(user_id)
        )
        return
    
    payment_time = payment_times[payment_id]
    current_time = datetime.now()
    
    if current_time - payment_time > timedelta(hours=1):
        await call.message.edit_text(
            "⏰ Время ожидания платежа истекло (1 час)\n\n❌ Платеж отменен.",
            reply_markup=user_menu(user_id)
        )
        del payment_times[payment_id]
        return
    
    await call.message.edit_text(
        "🔍 Проверяем блокчейн транзакции...",
        reply_markup=crypto_refill_waiting_inl(amount, payment_id)
    )
    
    # Простейшая заглушка вместо реального API
    if hasattr(config, 'bscscan_api_key') and config.bscscan_api_key:
        result = await check_usdt_transaction(
            wallet_address=config.crypto_wallet_address,
            amount=amount,
            api_key=config.bscscan_api_key,
            payment_time=payment_time,
            time_limit_hours=1
        )
    else:
        result = {'found': False, 'error': 'BSCScan API key not configured'}
    
    if result['found']:
        # Транзакция найдена
        user = get_user(id=user_id)
        # Зачисляем исходную сумму без копеек
        original_amount = amount - (amount % 1)  # Убираем копейки
        new_balance = update_user_balance_and_refill(user_id, original_amount)
        
        add_used_transaction_db(result['hash'], user_id, original_amount)
        add_refill(
            amount=original_amount,
            way="USDT BEP-20", 
            user_id=user_id,
            user_name=user.get('user_name', ''),
            first_name=user.get('first_name', ''),
            comment=f"USDT BEP-20 - {result['hash'][:10]}..."
        )
        
        del payment_times[payment_id]
        
        success_text = f"""✅ Криптоплатеж подтвержден!

💰 Зачислено: ${original_amount} USDT
💳 Ваш баланс: ${new_balance}

Спасибо за пополнение!"""
        
        await call.message.edit_text(success_text, reply_markup=user_menu(user_id))
        
    elif result['error']:
        await call.message.edit_text(
            f"❌ Ошибка проверки: {result['error']}\n\n🔄 Попробуйте позже",
            reply_markup=crypto_refill_waiting_inl(amount, payment_id)
        )
    else:
        remaining_time = ""
        elapsed = datetime.now() - payment_time
        remaining = timedelta(hours=1) - elapsed
        if remaining.total_seconds() > 0:
            minutes = int(remaining.total_seconds() / 60)
            remaining_time = f"\n⏰ Осталось времени: {minutes} минут"
        
        await call.message.edit_text(
            f"🔍 Транзакция не найдена\n\n💡 Убедитесь что:\n• Вы отправили точно ${amount} USDT\n• Использовали сеть BEP-20 (BSC){remaining_time}",
            reply_markup=crypto_refill_waiting_inl(amount, payment_id)
        )

@router.callback_query(F.data.startswith("check_crypto_again:"))
async def check_crypto_again(call: CallbackQuery):
    """Повторная проверка криптоплатежа"""
    user_id = call.from_user.id
    
    data = call.data.split(":")
    amount = float(data[1])
    payment_id = data[2]
    
    if payment_id not in payment_times:
        await call.message.edit_text(
            "❌ Данные о платеже не найдены.",
            reply_markup=user_menu(user_id)
        )
        return
    
    payment_time = payment_times[payment_id]
    if datetime.now() - payment_time > timedelta(hours=1):
        await call.message.edit_text(
            "⏰ Время ожидания платежа истекло (1 час)",
            reply_markup=user_menu(user_id)
        )
        del payment_times[payment_id]
        return
    
    await call.answer("🔍 Проверяем снова...", show_alert=True)
    
    # Имитируем проверку через API
    await check_crypto_payment(call)

@router.callback_query(F.data.startswith("cancel_crypto_waiting:"))
async def cancel_crypto_waiting(call: CallbackQuery):
    """Отмена ожидания криптоплатежа"""
    user_id = call.from_user.id
    
    data = call.data.split(":")
    payment_id = data[1] if len(data) > 1 else None
    
    if payment_id and payment_id in payment_times:
        del payment_times[payment_id]
    
    await call.message.edit_text(
        "❌ Ожидание платежа отменено",
        reply_markup=user_menu(user_id)
    )

@router.callback_query(F.data.startswith("cancel_crypto:"))
async def cancel_crypto_payment(call: CallbackQuery):
    """Отмена криптоплатежа"""
    user_id = call.from_user.id
    
    data = call.data.split(":")
    payment_id = data[1] if len(data) > 1 else None
    
    if payment_id and payment_id in payment_times:
        del payment_times[payment_id]
    
    await call.message.edit_text(
        "❌ Платеж отменен",
        reply_markup=user_menu(user_id)
    )

@router.callback_query(F.data == "cancel_refill")
async def cancel_refill_state(call: CallbackQuery, state: FSMContext):
    """Отмена процесса пополнения"""
    await state.clear()
    user_id = call.from_user.id
    
    await call.message.edit_text(
        "❌ Пополнение отменено",
        reply_markup=user_menu(user_id)
    )

@router.callback_query(F.data.startswith("check_crypto_polygon:"))
async def check_crypto_polygon_payment(call: CallbackQuery):
    """Проверка криптоплатежа в сети Polygon"""
    user_id = call.from_user.id
    lang = get_user_language(user_id)
    
    data = call.data.split(":")
    amount = float(data[1])
    payment_id = data[2]
    
    print(f"\n🚀 POLYGON CHECK: Пользователь {user_id} проверяет платеж ${amount}")
    
    if payment_id not in payment_times:
        await call.message.edit_text(
            get_text(lang, 'crypto_payment_not_found'),
            reply_markup=user_menu(user_id)
        )
        return
    
    payment_time = payment_times[payment_id]
    current_time = datetime.now()
    
    if current_time - payment_time > timedelta(hours=1):
        await call.message.edit_text(
            get_text(lang, 'crypto_payment_expired'),
            reply_markup=user_menu(user_id)
        )
        del payment_times[payment_id]
        return
    
    await call.message.edit_text(
        get_text(lang, 'crypto_checking_blockchain'),
        reply_markup=crypto_refill_waiting_inl(amount, payment_id)
    )
    
    # Проверяем через Polygonscan API
    if hasattr(config, 'polygonscan_api_key') and config.polygonscan_api_key:
        result = await check_usdt_transaction_polygon(
            wallet_address=config.crypto_wallet_address,
            amount=amount,
            api_key=config.polygonscan_api_key,  # Используем правильный ключ для Polygon
            payment_time=payment_time,
            time_limit_hours=1
        )
    else:
        result = {'found': False, 'error': 'Polygonscan API key not configured'}
    
    if result['found']:
        # Транзакция найдена
        user = get_user(id=user_id)
        # Зачисляем исходную сумму без копеек
        original_amount = amount - (amount % 1)  # Убираем копейки
        new_balance = update_user_balance_and_refill(user_id, original_amount)
        
        add_used_transaction_db(result['hash'], user_id, original_amount)
        add_refill(
            amount=original_amount,
            way="USDT Polygon", 
            user_id=user_id,
            user_name=user.get('user_name', ''),
            first_name=user.get('first_name', ''),
            comment=f"USDT Polygon - {result['hash'][:10]}..."
        )
        
        del payment_times[payment_id]
        
        success_text = get_text(lang, 'crypto_payment_confirmed', amount=original_amount, new_balance=new_balance)
        
        await call.message.edit_text(success_text, reply_markup=user_menu(user_id))
        
    elif result['error']:
        await call.message.edit_text(
            get_text(lang, 'crypto_check_error', error=result['error']),
            reply_markup=crypto_refill_waiting_inl(amount, payment_id)
        )
    else:
        remaining_time = ""
        elapsed = datetime.now() - payment_time
        remaining = timedelta(hours=1) - elapsed
        if remaining.total_seconds() > 0:
            minutes = int(remaining.total_seconds() / 60)
            remaining_time = f"\n⏰ Осталось времени: {minutes} минут"
        
        await call.message.edit_text(
            get_text(lang, 'crypto_transaction_not_found_polygon', amount=amount, remaining_time=remaining_time),
            reply_markup=crypto_refill_waiting_inl(amount, payment_id)
        )

@router.callback_query(F.data.startswith("check_crypto_erc20:"))
async def check_crypto_erc20_payment(call: CallbackQuery):
    """Проверка криптоплатежа в сети ERC-20"""
    user_id = call.from_user.id
    lang = get_user_language(user_id)
    
    data = call.data.split(":")
    amount = float(data[1])
    payment_id = data[2]
    
    print(f"\n🚀 ERC-20 CHECK: Пользователь {user_id} проверяет платеж ${amount}")
    
    if payment_id not in payment_times:
        await call.message.edit_text(
            get_text(lang, 'crypto_payment_not_found'),
            reply_markup=user_menu(user_id)
        )
        return
    
    payment_time = payment_times[payment_id]
    current_time = datetime.now()
    
    if current_time - payment_time > timedelta(hours=1):
        await call.message.edit_text(
            get_text(lang, 'crypto_payment_expired'),
            reply_markup=user_menu(user_id)
        )
        del payment_times[payment_id]
        return
    
    await call.message.edit_text(
        get_text(lang, 'crypto_checking_blockchain'),
        reply_markup=crypto_refill_waiting_inl(amount, payment_id)
    )
    
    # Проверяем через Etherscan API
    if hasattr(config, 'etherscan_api_key') and config.etherscan_api_key:
        result = await check_usdt_transaction_erc20(
            wallet_address=config.crypto_wallet_address,
            amount=amount,
            api_key=config.etherscan_api_key,
            payment_time=payment_time,
            time_limit_hours=1
        )
    else:
        result = {'found': False, 'error': 'Etherscan API key not configured'}
    
    if result['found']:
        # Транзакция найдена
        user = get_user(id=user_id)
        # Зачисляем исходную сумму без копеек
        original_amount = amount - (amount % 1)  # Убираем копейки
        new_balance = update_user_balance_and_refill(user_id, original_amount)
        
        add_used_transaction_db(result['hash'], user_id, original_amount)
        add_refill(
            amount=original_amount,
            way="USDT ERC-20", 
            user_id=user_id,
            user_name=user.get('user_name', ''),
            first_name=user.get('first_name', ''),
            comment=f"USDT ERC-20 - {result['hash'][:10]}..."
        )
        
        del payment_times[payment_id]
        
        success_text = get_text(lang, 'crypto_payment_confirmed', amount=original_amount, new_balance=new_balance)
        
        await call.message.edit_text(success_text, reply_markup=user_menu(user_id))
        
    elif result['error']:
        await call.message.edit_text(
            get_text(lang, 'crypto_check_error', error=result['error']),
            reply_markup=crypto_refill_waiting_inl(amount, payment_id)
        )
    else:
        remaining_time = ""
        elapsed = datetime.now() - payment_time
        remaining = timedelta(hours=1) - elapsed
        if remaining.total_seconds() > 0:
            minutes = int(remaining.total_seconds() / 60)
            remaining_time = f"\n⏰ Осталось времени: {minutes} минут"
        
        await call.message.edit_text(
            get_text(lang, 'crypto_transaction_not_found_erc20', amount=amount, remaining_time=remaining_time),
            reply_markup=crypto_refill_waiting_inl(amount, payment_id)
        )

async def process_crypto_erc20_payment(message: Message, state: FSMContext, amount: float):
    """Обработка пополнения через USDT в сети ERC-20"""
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    
    print(f"\n💰 CRYPTO ERC-20 CREATE: Создание криптоплатежа ERC-20 для пользователя {user_id}")
    print(f"💰 Запрошенная сумма: ${amount}")
    
    # Базовая проверка конфигурации
    if not hasattr(config, 'crypto_wallet_address') or not config.crypto_wallet_address or not hasattr(config, 'bscscan_api_key') or not config.bscscan_api_key or not hasattr(config, 'polygonscan_api_key') or not config.polygonscan_api_key or not hasattr(config, 'etherscan_api_key') or not config.etherscan_api_key or not hasattr(config, 'crypto_private_key') or not config.crypto_private_key:
        print(f"❌ CRYPTO ERC-20 CREATE: Криптоплатежи не настроены")
        await message.answer(get_text(lang, 'crypto_unavailable'))
        await state.clear()
        return

    # Проверка валидности приватного ключа для ERC-20 сети
    key_validation = validate_private_key_for_network(config.crypto_private_key, 'erc20')
    if not key_validation['valid']:
        print(f"❌ CRYPTO ERC-20 CREATE: {key_validation['error']}")
        await message.answer(get_text(lang, 'crypto_config_error'))
        await state.clear()
        return
    
    # Генерируем уникальный ID платежа
    payment_id = f"crypto_erc20_{user_id}_{int(time.time())}"
    
    # Генерируем сумму с копейками для идентификации
    crypto_service = CryptoUSDT(config.crypto_wallet_address, config.crypto_private_key, config.bscscan_api_key, config.polygonscan_api_key, config.etherscan_api_key)
    exact_amount = crypto_service.generate_payment_amount(amount)
    
    # Сохраняем время создания платежа
    payment_times[payment_id] = datetime.now()
    print(f"💾 CRYPTO ERC-20 CREATE: Сохранено время платежа {payment_id}: {payment_times[payment_id]}")
    
    # Текст с инструкциями
    crypto_text = f"""💰 Пополнение через USDT ERC-20

💰 Сумма к пополнению: <code>{exact_amount}</code>
📍 Адрес кошелька:
<code>{config.crypto_wallet_address}</code>

⚠️ ВАЖНО! Переведите точно <code>{exact_amount}</code> USDT в сети ERC-20
💡 Дополнительные копейки нужны для автоматической идентификации вашего платежа

⏰ Время на перевод: 1 час
💰 На баланс зачислится полная сумма пополнения с копейками
🔄 После перевода нажмите "Проверить платеж"

Платеж автоматически отменится через 1 час"""
    
    await message.answer(crypto_text, reply_markup=crypto_refill_erc20_inl(exact_amount, payment_id), parse_mode="HTML")
    await state.clear()

async def check_usdt_transaction_erc20(wallet_address, amount, api_key, payment_time, time_limit_hours=1):
    """Проверка транзакций USDT в сети Ethereum через Etherscan API"""
    try:
        print(f"🔍 ERC-20 CHECK: Проверяем транзакции для {wallet_address}")
        print(f"💰 Ожидаемая сумма: {amount} USDT")
        
        start_time = int(payment_time.timestamp()) - 300  # 5 минут до создания платежа
        end_time = int(time.time()) + 300  # 5 минут после текущего времени
        
        url = "https://api.etherscan.io/api"
        params = {
            'module': 'account',
            'action': 'tokentx',
            'contractaddress': '0xdAC17F958D2ee523a2206206994597C13D831ec7',  # USDT ERC-20 contract
            'address': wallet_address,
            'page': 1,
            'offset': 100,
            'startblock': 0,
            'endblock': 99999999,
            'sort': 'desc',
            'apikey': api_key
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                print(f"📡 ERC-20 API: Статус ответа: {response.status}")
                
                if response.status == 200:
                    data = await response.json()
                    
                    if data['status'] == '1' and data['result']:
                        transactions = data['result']
                        print(f"📋 ERC-20: Найдено {len(transactions)} транзакций")
                        
                        for i, tx in enumerate(transactions):
                            if i >= 10:  # Проверяем только первые 10
                                break
                                
                            if tx['to'].lower() == wallet_address.lower():
                                tx_time = int(tx['timeStamp'])
                                if start_time <= tx_time <= end_time:
                                    if is_transaction_used_db(tx['hash']):
                                        continue
                                    
                                    tx_amount = float(tx['value']) / (10**18)
                                    
                                    if abs(tx_amount - amount) < 0.001:
                                        print(f"✅ ERC-20: НАЙДЕНА ТРАНЗАКЦИЯ: {tx['hash']}")
                                        return {
                                            'found': True,
                                            'hash': tx['hash'],
                                            'amount': tx_amount,
                                            'from': tx['from'],
                                            'timestamp': tx_time
                                        }
                    
                    return {'found': False, 'error': None}
                else:
                    return {'found': False, 'error': f'Etherscan API error: {response.status}'}
                    
    except Exception as e:
        print(f"💥 ERC-20 DEBUG: Ошибка: {str(e)}")
        return {'found': False, 'error': str(e)} 