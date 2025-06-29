# - *- coding: utf- 8 - *-
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime

from tgbot.services.sqlite import (
    get_user, get_position, get_items_simple, buy_item, add_purchase, 
    update_user_balance, get_settings, get_positions_simple
)
from tgbot.keyboards.inline_user import (
    user_menu, products_inl, pos_buy_inl, choose_buy_items, 
    back_to_user_menu
)
from tgbot.utils.translations import get_text, get_user_language
from tgbot.data.loader import bot

# Создаём роутер для этого модуля
router = Router()

class ProductStates(StatesGroup):
    waiting_quantity = State()

@router.callback_query(F.data == "products:open")
async def products_open(call: CallbackQuery, state: FSMContext):
    """Открытие каталога товаров"""
    await state.clear()
    user_id = call.from_user.id
    lang = get_user_language(user_id)
    
    # Проверяем включены ли покупки
    settings = get_settings()
    if not settings or settings.get('is_buy') != "True":
        await call.answer(get_text(lang, 'buy_disabled'), show_alert=True)
        return
    
    text = get_text(lang, 'choose_product')
    await call.message.edit_text(text, reply_markup=products_inl(user_id))

@router.callback_query(F.data.startswith("buy_pos:"))
async def buy_position(call: CallbackQuery, state: FSMContext):
    """Выбор товара для покупки"""
    user_id = call.from_user.id
    lang = get_user_language(user_id)
    
    pos_id = int(call.data.split(":")[1])
    position = get_position(pos_id=pos_id)
    
    if not position:
        await call.answer(get_text(lang, 'product_not_found'), show_alert=True)
        return
    
    items_count = len(get_items_simple(pos_id))
    if items_count == 0:
        await call.answer(get_text(lang, 'product_out_of_stock'), show_alert=True)
        return
    
    text = get_text(lang, 'product_info', 
                   name=position['name'], 
                   description=position['description'],
                   price=position['price'],
                   items_count=items_count)
    
    await call.message.edit_text(text, reply_markup=pos_buy_inl(pos_id))

@router.callback_query(F.data.startswith("buy_pos_count:"))
async def buy_position_count(call: CallbackQuery, state: FSMContext):
    """Покупка определенного количества товара"""
    user_id = call.from_user.id
    lang = get_user_language(user_id)
    
    data = call.data.split(":")
    pos_id = int(data[1])
    count = int(data[2])
    
    position = get_position(pos_id=pos_id)
    if not position:
        await call.answer(get_text(lang, 'product_changed'), show_alert=True)
        await call.message.edit_text(get_text(lang, 'product_changed'), 
                                   reply_markup=user_menu(user_id))
        return
    
    items = get_items_simple(pos_id)
    if len(items) < count:
        await call.answer(get_text(lang, 'not_enough_items'), show_alert=True)
        return
    
    user = get_user(id=user_id)
    total_price = position['price'] * count
    
    if user['balance'] < total_price:
        await call.answer(get_text(lang, 'insufficient_balance'), show_alert=True)
        return
    
    # Подтверждение покупки
    if count == 1:
        confirm_text = get_text(lang, 'confirm_buy_one', name=position['name'])
    else:
        confirm_text = get_text(lang, 'confirm_buy_many', name=position['name'], amount=count)
    
    await call.message.edit_text(confirm_text, reply_markup=choose_buy_items(pos_id, count))

@router.callback_query(F.data.startswith("confirm_buy:"))
async def confirm_buy(call: CallbackQuery, state: FSMContext):
    """Подтверждение покупки"""
    user_id = call.from_user.id
    lang = get_user_language(user_id)
    
    data = call.data.split(":")
    pos_id = int(data[1])
    count = int(data[2])
    
    position = get_position(pos_id=pos_id)
    if not position:
        await call.answer(get_text(lang, 'product_changed'), show_alert=True)
        await call.message.edit_text(get_text(lang, 'product_changed'), 
                                   reply_markup=user_menu(user_id))
        return
    
    items = get_items_simple(pos_id)
    if len(items) < count:
        await call.answer(get_text(lang, 'product_changed'), show_alert=True)
        await call.message.edit_text(get_text(lang, 'product_changed'), 
                                   reply_markup=user_menu(user_id))
        return
    
    user = get_user(id=user_id)
    total_price = position['price'] * count
    
    if user['balance'] < total_price:
        await call.answer(get_text(lang, 'insufficient_balance'), show_alert=True)
        return
    
    # Покупаем товары
    purchased_items_data, actual_count, _ = buy_item(items[:count], count, position['infinity'])
    
    # Обновляем баланс пользователя
    new_balance = user['balance'] - total_price
    update_user_balance(user_id, new_balance)
    
    # Добавляем запись о покупке
    buy_time = datetime.now().strftime("%d.%m.%Y %H:%M")
    receipt = f"buy_{user_id}_{int(datetime.now().timestamp())}"
    
    add_purchase(
        user_id=user_id,
        first_name=user.get('first_name', ''),
        user_name=user.get('user_name', ''),
        receipt=receipt,
        count=count,
        price=total_price,
        position_id=pos_id,
        position_name=position['name'],
        item="\n".join(purchased_items_data),
        date=buy_time,
        date_unix=int(datetime.now().timestamp())
    )
    
    # Формируем список купленных товаров для отображения
    items_text = "\n".join([f"<code>{item}</code>" for item in purchased_items_data])
    
    success_text = get_text(lang, 'purchase_success',
                           receipt=receipt,
                           name=position['name'],
                           amount=count,
                           amount_pay=total_price,
                           buy_time=buy_time,
                           items=items_text)
    
    await call.message.edit_text(success_text, reply_markup=user_menu(user_id), parse_mode="HTML")
    
    # Уведомляем админов о покупке
    try:
        admin_settings = get_settings()
        if admin_settings and admin_settings.get('is_notify') == "True":
            # Используем русский язык для админских уведомлений по умолчанию
            # Позже можно добавить настройку языка для админов
            admin_lang = 'ru'
            user_name = user.get('first_name', get_text(admin_lang, 'unknown_user'))
            username = user.get('user_name', get_text(admin_lang, 'no_username'))
            
            admin_text = get_text(admin_lang, 'admin_new_purchase',
                                 user_name=user_name,
                                 username=username, 
                                 product_name=position['name'],
                                 count=count,
                                 total_price=total_price)
            
            # Здесь должна быть отправка уведомления админам
            # Пока что пропускаем, так как нужен список админов
            pass
    except Exception as e:
        print(f"Ошибка отправки уведомления админам: {e}")

@router.callback_query(F.data == "buy_pos_count_custom")
async def buy_custom_count(call: CallbackQuery, state: FSMContext):
    """Ввод произвольного количества товара"""
    user_id = call.from_user.id
    lang = get_user_language(user_id)
    
    # Получаем pos_id из предыдущего состояния или из callback_data
    # Пока что возвращаем к выбору товара
    text = get_text(lang, 'enter_quantity')
    await call.message.edit_text(text, reply_markup=back_to_user_menu(user_id))
    await state.set_state(ProductStates.waiting_quantity)

@router.message(ProductStates.waiting_quantity)
async def process_custom_quantity(message: Message, state: FSMContext):
    """Обработка произвольного количества"""
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    
    try:
        quantity = int(message.text)
        if quantity <= 0:
            await message.answer(get_text(lang, 'invalid_quantity'))
            return
        
        # Здесь должна быть логика для обработки произвольного количества
        # Пока что просто очищаем состояние и возвращаем в меню
        await state.clear()
        await message.answer(get_text(lang, 'quantity_processed'), reply_markup=user_menu(user_id))
        
    except ValueError:
        await message.answer(get_text(lang, 'quantity_must_be_number'))

# TODO: Добавить обработчики пользовательских товаров после основной миграции 