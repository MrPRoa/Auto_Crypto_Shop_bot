# - *- coding: utf- 8 - *-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tgbot.services.sqlite import get_settings, get_payments, get_all_categories, get_positions, get_items, \
get_pod_category, get_pod_categories, get_position, get_positions_simple, get_items_simple
from tgbot.data import config
from tgbot.utils.utils_functions import get_admins
from tgbot.utils.translations import get_text, get_user_language

def language_selection():
    """Клавиатура выбора языка"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_language:ru"),
            InlineKeyboardButton(text="🇺🇸 English", callback_data="set_language:en")
        ]
    ])
    return keyboard

def language_selection_with_back(user_id):
    """Выбор языка с кнопкой возврата в профиль"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_language:ru"),
            InlineKeyboardButton(text="🇺🇸 English", callback_data="set_language:en")
        ],
        [InlineKeyboardButton(text="⬅ Вернуться", callback_data="profile:open")]
    ])
    return keyboard

def sub():
    """Клавиатура для подписки на канал"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Подписаться", url="https://t.me/your_channel")],
        [InlineKeyboardButton(text="✅ Проверить подписку", callback_data="check_sub")]
    ])
    return keyboard

def user_menu(user_id):
    """Главное меню пользователя"""
    lang = get_user_language(user_id)
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text(lang, 'products'), callback_data="products:open")],
        [InlineKeyboardButton(text=get_text(lang, 'profile'), callback_data="profile:open")],
        [InlineKeyboardButton(text=get_text(lang, 'refill'), callback_data="refill")],
        [
            InlineKeyboardButton(text=get_text(lang, 'faq'), callback_data="FAQ"),
            InlineKeyboardButton(text=get_text(lang, 'support'), callback_data="support")
        ]
    ])
    
    # Добавляем кнопку администратора для админов
    if user_id in get_admins():
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(text="⚙️ Администратор", callback_data="admin_menu")
        ])

    return keyboard

def faq_inl():
    news = get_settings()['news']
    chat = get_settings()['chat']

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=faq_chat_inl, url=chat),
            InlineKeyboardButton(text=faq_news_inl, url=news)
        ]
    ])
    return keyboard

def support_inll():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=support_inl, url=get_settings()['support'])]
    ])
    return keyboard

def chat_inl():
    link = get_settings()['chat']
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=faq_chat_inl, url=link)]
    ])
    return keyboard

def news_inl():
    link = get_settings()['news']
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=faq_news_inl, url=link)]
    ])
    return keyboard

def profile_inl(user_id):
    """Клавиатура профиля"""
    lang = get_user_language(user_id)
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text(lang, 'ref_system'), callback_data="ref_system")],
        [InlineKeyboardButton(text=get_text(lang, 'promocode'), callback_data="promocode")],
        [InlineKeyboardButton(text=get_text(lang, 'last_purchases'), callback_data="last_purchases")],
        [InlineKeyboardButton(text=get_text(lang, 'language_btn'), callback_data="change_language")],
        [InlineKeyboardButton(text=get_text(lang, 'back'), callback_data="back_to_menu")]
    ])
    return keyboard

def back_to_profile(user_id):
    """Кнопка возврата к профилю"""
    lang = get_user_language(user_id)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text(lang, 'back'), callback_data="profile:open")]
    ])
    return keyboard

def back_to_user_menu(user_id):
    """Кнопка возврата в главное меню"""
    lang = get_user_language(user_id)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text(lang, 'back'), callback_data="back_to_menu")]
    ])
    return keyboard

def close_inl():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=close_text, callback_data="close_text_mail")]
    ])
    return keyboard

def refill_open_inl(method, amount, payment_url, payment_id):
    """Клавиатура открытия платежа"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 Оплатить", url=payment_url)],
        [InlineKeyboardButton(text="✅ Проверить платеж", callback_data=f"check_opl:{method}:{amount}:{payment_id}")],
        [InlineKeyboardButton(text="❌ Отменить", callback_data="back_to_menu")]
    ])
    return keyboard

def refill_inl():
    """Клавиатура способов пополнения"""
    payments = get_payments()
    kb = []

    if payments:
        if payments.get('pay_yoomoney') == "True":
            kb.append([InlineKeyboardButton(text="💳 ЮMoney", callback_data="refill:yoomoney")])
        if payments.get('pay_lava') == "True":
            kb.append([InlineKeyboardButton(text="🌋 Lava", callback_data="refill:lava")])
        if payments.get('pay_crystal') == "True":
            kb.append([InlineKeyboardButton(text="💎 Crystal", callback_data="refill:crystal")])
        if payments.get('pay_lolz') == "True":
            kb.append([InlineKeyboardButton(text="⚡ Lolz", callback_data="refill:lolz")])
    
    # Криптовалюта всегда доступна
    kb.append([InlineKeyboardButton(text="₿ USDT BEP-20", callback_data="refill:crypto_usdt")])
    kb.append([InlineKeyboardButton(text="🔷 USDT Polygon", callback_data="refill:crypto_usdt_polygon")])
    kb.append([InlineKeyboardButton(text="🔵 USDT ERC-20", callback_data="refill:crypto_usdt_erc20")])
    kb.append([InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_menu")])

    return InlineKeyboardMarkup(inline_keyboard=kb)

def open_products():
    kb = []
    for category in get_all_categories():
        name = category['name']
        cat_id = category['id']
        kb.append([InlineKeyboardButton(text=name, callback_data=f"open_category:{cat_id}")])

    kb.append([InlineKeyboardButton(text=back, callback_data="back_to_user_menu")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard

def open_pod_cat_positions(pod_cat_id):
    kb = []
    for pos in get_positions(pod_cat_id=pod_cat_id):
        name = pos['name']
        pos_id = pos['id']
        price = pos['price']
        items = f"{len(get_items(position_id=pos_id))}шт"
        if pos['infinity'] == "+":
            items = "[Безлимит]"

        kb.append([InlineKeyboardButton(text=f"{name} | {price}$ | {items}", callback_data=f"buy_pos:{pos_id}")])

    pod_cat = get_pod_category(pod_cat_id)
    kb.append([InlineKeyboardButton(text=back, callback_data=f"open_pod_category:{pod_cat['category_id']}")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard

def open_positions(cat_id):
    kb = []
    for pod_cat in get_pod_categories(cat_id):
        pod_cat_name = pod_cat['name']
        pod_cat_id = pod_cat['id']
        kb.append([InlineKeyboardButton(text=pod_cat_name, callback_data=f"open_pod_category:{pod_cat_id}")])

    kb.append([InlineKeyboardButton(text=back, callback_data="products:open")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard

def pos_buy_inl(pos_id):
    """Клавиатура покупки товара"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1️⃣", callback_data=f"buy_pos_count:{pos_id}:1")],
        [InlineKeyboardButton(text="5️⃣", callback_data=f"buy_pos_count:{pos_id}:5")],
        [InlineKeyboardButton(text="🔢 Другое количество", callback_data="buy_pos_count_custom")],
        [InlineKeyboardButton(text="⬅ Назад", callback_data="products:open")]
    ])
    return keyboard

def choose_buy_items(pos_id, count):
    """Клавиатура подтверждения покупки"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Купить", callback_data=f"confirm_buy:{pos_id}:{count}")],
        [InlineKeyboardButton(text="❌ Отменить", callback_data="products:open")]
    ])
    return keyboard

def crypto_refill_inl(amount, payment_id):
    """Клавиатура криптопополнения"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Проверить платеж", callback_data=f"check_crypto:{amount}:{payment_id}")],
        [InlineKeyboardButton(text="❌ Отменить", callback_data=f"cancel_crypto:{payment_id}")]
    ])
    return keyboard

def crypto_refill_polygon_inl(amount, payment_id):
    """Клавиатура криптопополнения через Polygon"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Проверить платеж", callback_data=f"check_crypto_polygon:{amount}:{payment_id}")],
        [InlineKeyboardButton(text="❌ Отменить", callback_data=f"cancel_crypto:{payment_id}")]
    ])
    return keyboard

def crypto_refill_erc20_inl(amount, payment_id):
    """Клавиатура криптопополнения через ERC-20"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Проверить платеж", callback_data=f"check_crypto_erc20:{amount}:{payment_id}")],
        [InlineKeyboardButton(text="❌ Отменить", callback_data=f"cancel_crypto:{payment_id}")]
    ])
    return keyboard

def crypto_refill_waiting_inl(amount, payment_id):
    """Клавиатура ожидания криптоплатежа"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Проверить снова", callback_data=f"check_crypto_again:{amount}:{payment_id}")],
        [InlineKeyboardButton(text="❌ Отменить", callback_data=f"cancel_crypto_waiting:{payment_id}")]
    ])
    return keyboard

def cancel_refill_inl(user_id):
    """Клавиатура отмены пополнения"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_refill")]
    ])
    return keyboard

def products_inl(user_id):
    """Клавиатура товаров"""
    lang = get_user_language(user_id)
    positions = get_positions_simple()
    
    kb = []
    for position in positions:
        items_count = len(get_items_simple(position['id']))
        if items_count > 0:
            button_text = f"📦 {position['name']} (${position['price']}) - {items_count}шт"
            kb.append([InlineKeyboardButton(text=button_text, callback_data=f"buy_pos:{position['id']}")])

    kb.append([InlineKeyboardButton(text=get_text(lang, 'back'), callback_data="back_to_menu")])

    return InlineKeyboardMarkup(inline_keyboard=kb)