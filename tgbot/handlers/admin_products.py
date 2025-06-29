# - *- coding: utf- 8 - *-
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup

from tgbot.services.sqlite import (
    get_position, add_position_simple, delete_position_simple, get_positions_simple,
    get_items_simple, add_item_simple, delete_item_simple, update_position_simple
)
from tgbot.keyboards.inline_admin import (
    products_edits, add_product_inl, back_pr_edits, 
    edit_product_inl
)
from tgbot.filters.is_admin import IsAdmin
from tgbot.utils.translations import get_text, get_user_language

# Создаём роутер для этого модуля
router = Router()

class ProductStates(StatesGroup):
    add_name = State()
    add_description = State()
    add_price = State()
    add_infinity = State()
    add_items = State()
    edit_name = State()
    edit_description = State()
    edit_price = State()
    edit_items = State()

@router.callback_query(IsAdmin(), F.data == "add_product")
async def add_product_start(call: CallbackQuery, state: FSMContext):
    """Начало добавления товара"""
    await state.clear()
    await state.set_state(ProductStates.add_name)
    lang = get_user_language(call.from_user.id)
    await call.message.edit_text(get_text(lang, 'enter_product_name'), reply_markup=back_pr_edits())

@router.message(IsAdmin(), ProductStates.add_name)
async def add_product_name(message: Message, state: FSMContext):
    """Получение названия товара"""
    await state.update_data(name=message.text)
    await state.set_state(ProductStates.add_description)
    lang = get_user_language(message.from_user.id)
    await message.answer(get_text(lang, 'enter_product_description'))

@router.message(IsAdmin(), ProductStates.add_description)
async def add_product_description(message: Message, state: FSMContext):
    """Получение описания товара"""
    await state.update_data(description=message.text)
    await state.set_state(ProductStates.add_price)
    lang = get_user_language(message.from_user.id)
    await message.answer(get_text(lang, 'enter_product_price'))

@router.message(IsAdmin(), ProductStates.add_price)
async def add_product_price(message: Message, state: FSMContext):
    """Получение цены товара"""
    lang = get_user_language(message.from_user.id)
    try:
        price = float(message.text.replace(',', '.'))
        if price <= 0:
            await message.answer(get_text(lang, 'price_positive'))
            return
        
        await state.update_data(price=price)
        await state.set_state(ProductStates.add_infinity)
        
        await message.answer(get_text(lang, 'product_type_choice'), reply_markup=add_product_inl())
        
    except ValueError:
        await message.answer(get_text(lang, 'price_number'))

@router.callback_query(IsAdmin(), F.data.startswith("set_infinity:"))
async def set_product_infinity(call: CallbackQuery, state: FSMContext):
    """Установка типа товара"""
    infinity = call.data.split(":")[1] == "True"
    await state.update_data(infinity=infinity)
    await state.set_state(ProductStates.add_items)
    
    lang = get_user_language(call.from_user.id)
    if infinity:
        text = get_text(lang, 'enter_infinite_content')
    else:
        text = get_text(lang, 'enter_products_list')
    
    await call.message.edit_text(text)

@router.message(IsAdmin(), ProductStates.add_items)
async def add_product_items(message: Message, state: FSMContext):
    """Получение товаров и создание позиции"""
    data = await state.get_data()
    items_text = message.text
    lang = get_user_language(message.from_user.id)
    
    # Создаем позицию
    position_id = add_position_simple(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        infinity=data['infinity']
    )
    
    # Добавляем товары
    if data['infinity']:
        # Для бесконечного товара добавляем один элемент
        add_item_simple(position_id, items_text)
        items_count = "♾️"
        product_type = get_text(lang, 'infinite_type')
    else:
        # Для обычного товара добавляем каждую строку как отдельный товар
        items = items_text.strip().split('\n')
        for item in items:
            if item.strip():
                add_item_simple(position_id, item.strip())
        items_count = len([item for item in items if item.strip()])
        product_type = get_text(lang, 'regular_type')
    
    await state.clear()
    
    success_text = get_text(lang, 'product_added',
                           name=data['name'],
                           description=data['description'],
                           price=data['price'],
                           type=product_type,
                           count=items_count)
    
    await message.answer(success_text, reply_markup=products_edits())

@router.callback_query(IsAdmin(), F.data == "edit_products")
async def edit_products_list(call: CallbackQuery, state: FSMContext):
    """Список товаров для редактирования"""
    await state.clear()
    positions = get_positions_simple()
    lang = get_user_language(call.from_user.id)
    
    if not positions:
        await call.answer(get_text(lang, 'no_products_found'), show_alert=True)
        return
    
    text = get_text(lang, 'edit_products_list')
    await call.message.edit_text(text, reply_markup=edit_product_inl())

@router.callback_query(IsAdmin(), F.data == "back_to_products")
async def back_to_products(call: CallbackQuery, state: FSMContext):
    """Возврат к управлению товарами"""
    await state.clear()
    lang = get_user_language(call.from_user.id)
    await call.message.edit_text(get_text(lang, 'products_management'), reply_markup=products_edits())

@router.callback_query(IsAdmin(), F.data.startswith("edit_pos:"))
async def edit_product_menu(call: CallbackQuery, state: FSMContext):
    """Меню редактирования конкретного товара"""
    await state.clear()
    pos_id = int(call.data.split(":")[1])
    position = get_position(pos_id)
    
    if not position:
        lang = get_user_language(call.from_user.id)
        await call.answer(get_text(lang, 'product_not_found'), show_alert=True)
        return
    
    lang = get_user_language(call.from_user.id)
    items_count = len(get_items_simple(pos_id))
    items_display = "♾️" if position['infinity'] == "+" else f"{items_count}шт"
    
    text = get_text(lang, 'edit_product_menu',
                   name=position['name'],
                   description=position['description'],
                   price=position['price'],
                   items=items_display)
    
    await call.message.edit_text(text, reply_markup=product_edit_menu(pos_id))

@router.callback_query(IsAdmin(), F.data.startswith("edit_pos_name:"))
async def edit_product_name_start(call: CallbackQuery, state: FSMContext):
    """Начало редактирования названия"""
    pos_id = int(call.data.split(":")[1])
    await state.update_data(pos_id=pos_id)
    await state.set_state(ProductStates.edit_name)
    
    lang = get_user_language(call.from_user.id)
    await call.message.edit_text(get_text(lang, 'enter_new_product_name'))

@router.message(IsAdmin(), ProductStates.edit_name)
async def edit_product_name_finish(message: Message, state: FSMContext):
    """Сохранение нового названия"""
    data = await state.get_data()
    pos_id = data['pos_id']
    new_name = message.text
    
    update_position_simple(pos_id, name=new_name)
    await state.clear()
    
    lang = get_user_language(message.from_user.id)
    await message.answer(get_text(lang, 'product_name_updated', name=new_name))
    
    # Возвращаемся к меню редактирования товара
    position = get_position(pos_id)
    items_count = len(get_items_simple(pos_id))
    items_display = "♾️" if position['infinity'] == "+" else f"{items_count}шт"
    
    text = get_text(lang, 'edit_product_menu',
                   name=position['name'],
                   description=position['description'], 
                   price=position['price'],
                   items=items_display)
    
    await message.answer(text, reply_markup=product_edit_menu(pos_id))

@router.callback_query(IsAdmin(), F.data.startswith("edit_pos_desc:"))
async def edit_product_desc_start(call: CallbackQuery, state: FSMContext):
    """Начало редактирования описания"""
    pos_id = int(call.data.split(":")[1])
    await state.update_data(pos_id=pos_id)
    await state.set_state(ProductStates.edit_description)
    
    lang = get_user_language(call.from_user.id)
    await call.message.edit_text(get_text(lang, 'enter_new_product_description'))

@router.message(IsAdmin(), ProductStates.edit_description)
async def edit_product_desc_finish(message: Message, state: FSMContext):
    """Сохранение нового описания"""
    data = await state.get_data()
    pos_id = data['pos_id']
    new_desc = message.text
    
    update_position_simple(pos_id, description=new_desc)
    await state.clear()
    
    lang = get_user_language(message.from_user.id)
    await message.answer(get_text(lang, 'product_description_updated'))
    
    # Возвращаемся к меню редактирования товара
    position = get_position(pos_id)
    items_count = len(get_items_simple(pos_id))
    items_display = "♾️" if position['infinity'] == "+" else f"{items_count}шт"
    
    text = get_text(lang, 'edit_product_menu',
                   name=position['name'],
                   description=position['description'],
                   price=position['price'],
                   items=items_display)
    
    await message.answer(text, reply_markup=product_edit_menu(pos_id))

@router.callback_query(IsAdmin(), F.data.startswith("edit_pos_price:"))
async def edit_product_price_start(call: CallbackQuery, state: FSMContext):
    """Начало редактирования цены"""
    pos_id = int(call.data.split(":")[1])
    await state.update_data(pos_id=pos_id)
    await state.set_state(ProductStates.edit_price)
    
    lang = get_user_language(call.from_user.id)
    await call.message.edit_text(get_text(lang, 'enter_new_product_price'))

@router.message(IsAdmin(), ProductStates.edit_price)
async def edit_product_price_finish(message: Message, state: FSMContext):
    """Сохранение новой цены"""
    data = await state.get_data()
    pos_id = data['pos_id']
    lang = get_user_language(message.from_user.id)
    
    try:
        new_price = float(message.text.replace(',', '.'))
        if new_price <= 0:
            await message.answer(get_text(lang, 'price_positive'))
            return
        
        update_position_simple(pos_id, price=new_price)
        await state.clear()
        
        await message.answer(get_text(lang, 'product_price_updated', price=new_price))
        
        # Возвращаемся к меню редактирования товара
        position = get_position(pos_id)
        items_count = len(get_items_simple(pos_id))
        items_display = "♾️" if position['infinity'] == "+" else f"{items_count}шт"
        
        text = get_text(lang, 'edit_product_menu',
                       name=position['name'],
                       description=position['description'],
                       price=position['price'],
                       items=items_display)
        
        await message.answer(text, reply_markup=product_edit_menu(pos_id))
        
    except ValueError:
        await message.answer(get_text(lang, 'price_number'))

@router.callback_query(IsAdmin(), F.data.startswith("delete_pos:"))
async def delete_product_confirm(call: CallbackQuery):
    """Подтверждение удаления товара"""
    pos_id = int(call.data.split(":")[1])
    
    lang = get_user_language(call.from_user.id)
    position = get_position(pos_id)
    
    if not position:
        await call.answer(get_text(lang, 'product_not_found'), show_alert=True)
        return
    
    text = get_text(lang, 'confirm_delete_product', name=position['name'])
    from tgbot.keyboards.inline_admin import confirm_delete_product
    await call.message.edit_text(text, reply_markup=confirm_delete_product(pos_id))

@router.callback_query(IsAdmin(), F.data.startswith("confirm_delete_pos:"))
async def delete_product_final(call: CallbackQuery):
    """Окончательное удаление товара"""
    pos_id = int(call.data.split(":")[1])
    position = get_position(pos_id)
    
    if position:
        delete_position_simple(pos_id)
        lang = get_user_language(call.from_user.id)
        await call.answer(get_text(lang, 'product_deleted', name=position['name']), show_alert=True)
    
    # Возвращаемся к списку товаров
    await edit_products_list(call, None) 