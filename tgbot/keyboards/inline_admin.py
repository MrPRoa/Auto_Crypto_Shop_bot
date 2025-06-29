# - *- coding: utf- 8 - *-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tgbot.services.sqlite import get_settings, get_user, get_all_categories, get_pod_categories, get_positions, get_items, get_positions_simple, get_items_simple
from tgbot.utils.translations import get_text

back = "⬅ Вернуться"
close = "❌ Закрыть"
qiwi_text = "🥝 QIWI"
yoomoney_text = "💳 ЮMoney"
lava_text = "🌋 LavaPay"
lzt_text = "⚡ LolzTeam"
crystalPay_text = "💎 Crystal Pay"


def admin_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🖤 Общие настройки", callback_data="settings")],
        [InlineKeyboardButton(text="🎲 Доп. настройки", callback_data="extra_settings")],
        [InlineKeyboardButton(text="❗ Выключатели", callback_data="on_off")],
        [InlineKeyboardButton(text="📊 Статистика", callback_data="stats")],
        [InlineKeyboardButton(text="🔍 Искать", callback_data="find:")],
        [InlineKeyboardButton(text="💎 Управление товарами", callback_data="pr_edit")],
        [InlineKeyboardButton(text="📌 Рассылка", callback_data="mail_start")],
        [InlineKeyboardButton(text="💰 Платежные системы", callback_data="payments")],
        [InlineKeyboardButton(text=back, callback_data="back_to_user_menu")]
    ])
    return keyboard

def back_sett():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=back, callback_data="settings_back")]
    ])
    return keyboard

def extra_back():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=back, callback_data="extra_settings")]
    ])
    return keyboard

def extra_settings_inl():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="💎 Создать промокод", callback_data="promo_create"),
            InlineKeyboardButton(text="🎲 Удалить промокод", callback_data="promo_delete")
        ],
        [InlineKeyboardButton(text="2️⃣ Изменить кол-во рефералов для 2 лвла", callback_data="ref_lvl_edit:2")],
        [InlineKeyboardButton(text="3️⃣ Изменить кол-во рефералов для 3 лвла", callback_data="ref_lvl_edit:3")],
        [InlineKeyboardButton(text=back, callback_data="settings_back")]
    ])
    return keyboard

def on_off_inl():
    work = get_settings()['is_work']
    purchases = get_settings()['is_buy']
    refills = get_settings()['is_refill']
    ref_system = get_settings()['is_ref']
    notify = get_settings()['is_notify']
    sub = get_settings()['is_sub']

    sub_emoji = "✅" if sub == "True" else "❌"
    notify_emoji = "✅" if notify == "True" else "❌"
    work_emoji = "✅" if work == "True" else "❌"
    buy_emoji = "✅" if purchases == "True" else "❌"
    refill_emoji = "✅" if refills == "True" else "❌"
    ref_emoji = "✅" if ref_system == "True" else "❌"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"Тех. Работы | {work_emoji}", callback_data="work:on_off")],
        [InlineKeyboardButton(text=f"Покупки | {buy_emoji}", callback_data="buys:on_off")],
        [InlineKeyboardButton(text=f"Пополнения | {refill_emoji}", callback_data="refills:on_off")],
        [InlineKeyboardButton(text=f"Реф. Система | {ref_emoji}", callback_data="ref:on_off")],
        [InlineKeyboardButton(text=f"Увед. О новых юзерах | {notify_emoji}", callback_data="notify:on_off")],
        [InlineKeyboardButton(text=f"Проверка подписки | {sub_emoji}", callback_data="sub:on_off")],
        [InlineKeyboardButton(text=back, callback_data="settings_back")]
    ])
    return keyboard

def settings_inl():
    faq = get_settings()['faq']
    support = get_settings()['support']
    chat = get_settings()['chat']
    news = get_settings()['news']
    ref_percent_1 = get_settings()['ref_percent_1']
    ref_percent_2 = get_settings()['ref_percent_2']
    ref_percent_3 = get_settings()['ref_percent_3']

    faq_emoji = "❌" if faq is None or faq == "-" or faq == "None" else "✅"
    sup_emoji = "❌" if support is None or support == "-" or support == "None" else "✅"
    chat_emoji = "❌" if chat is None or chat == "-" or chat == "None" else "✅"
    news_emoji = "❌" if news is None or news == "-" or news == "None" else "✅"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"FAQ | {faq_emoji}", callback_data="faq:edit")],
        [InlineKeyboardButton(text=f"Тех. Поддержка | {sup_emoji}", callback_data="sup:edit")],
        [InlineKeyboardButton(text=f"Чат | {chat_emoji}", callback_data="chat:edit")],
        [InlineKeyboardButton(text=f"Новостной | {news_emoji}", callback_data="news:edit")],
        [InlineKeyboardButton(text=f"Реф. Процент 1 лвл. | {ref_percent_1}%", callback_data="ref_percent:edit:1")],
        [InlineKeyboardButton(text=f"Реф. Процент 2 лвл. | {ref_percent_2}%", callback_data="ref_percent:edit:2")],
        [InlineKeyboardButton(text=f"Реф. Процент 3 лвл. | {ref_percent_3}%", callback_data="ref_percent:edit:3")],
        [InlineKeyboardButton(text=back, callback_data="settings_back")]
    ])
    return keyboard

def find_back():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=back, callback_data="find:back")]
    ])
    return keyboard


def profile_adm_inl(user_id):
    user = get_user(id=user_id)

    ban_button = InlineKeyboardButton(
        text="⛔ Разблокировать" if user['is_ban'] == "True" else "⛔ Заблокировать",
        callback_data=f"user:is_ban_unban:{user_id}" if user['is_ban'] == "True" else f"user:is_ban_ban:{user_id}"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 Выдать баланс", callback_data=f"user:balance_add:{user_id}")],
        [InlineKeyboardButton(text="💰 Изменить баланс", callback_data=f"user:balance_edit:{user_id}")],
        [ban_button],
        [InlineKeyboardButton(text="⭐ Отправить уведомление", callback_data=f"user:sms:{user_id}")],
        [InlineKeyboardButton(text=back, callback_data="find:back")]
    ])
    return keyboard


def find_settings():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👤 Профиль", callback_data="find:profile")],
        [InlineKeyboardButton(text="🧾 Чек", callback_data="find:receipt")],
        [InlineKeyboardButton(text=back, callback_data="settings_back")]
    ])
    return keyboard

def payments_settings():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=qiwi_text, callback_data="payments:qiwi")],
        [InlineKeyboardButton(text=yoomoney_text, callback_data="payments:yoomoney")],
        [InlineKeyboardButton(text=lava_text, callback_data="payments:lava")],
        [InlineKeyboardButton(text=lzt_text, callback_data="payments:lzt")],
        [InlineKeyboardButton(text=crystalPay_text, callback_data="payments:crystalPay")],
        [InlineKeyboardButton(text=back, callback_data="settings_back")]
    ])
    return keyboard

def payments_settings_info(way, status):
    status_emoji = "✅" if status == "True" else "❌"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"Вкл/Выкл | {status_emoji}", callback_data=f"payments_on_off:{way}:{'off' if status == 'True' else 'on'}")],
        [
            InlineKeyboardButton(text="💰 Узнать баланс", callback_data=f"payments_balance:{way}"),
            InlineKeyboardButton(text="📌 Показать информацию", callback_data=f"payments_info:{way}")
        ],
        [InlineKeyboardButton(text=back, callback_data="payments")]
    ])
    return keyboard

def set_back():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=back, callback_data="set_back")]
    ])
    return keyboard

def payments_back():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=back, callback_data="payments")]
    ])
    return keyboard

def mail_types():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Текст", callback_data="mail:text")],
        [InlineKeyboardButton(text="🖼 Фото + Текст", callback_data="mail:photo")],
        [InlineKeyboardButton(text=back, callback_data="settings_back")]
    ])
    return keyboard

def opr_mail_text():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Отправить", callback_data="mail_start_text:yes"),
            InlineKeyboardButton(text="❌ Отменить", callback_data="mail_start_text:no")
        ]
    ])
    return keyboard

def opr_mail_photo():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Отправить", callback_data="mail_start_photo:yes"),
            InlineKeyboardButton(text="❌ Отменить", callback_data="mail_start_photo:no")
        ]
    ])
    return keyboard

def products_edits():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Добавить товар", callback_data="add_product")],
        [InlineKeyboardButton(text="✏️ Редактировать товары", callback_data="edit_products")],
        [InlineKeyboardButton(text=back, callback_data="settings_back")]
    ])
    return keyboard

def back_pr_edits():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=back, callback_data="pr_edit")]
    ])
    return keyboard

def open_cats_for_edit():
    keyboard = InlineKeyboardMarkup()

    for category in get_all_categories():
        name = category['name']
        cat_id = category['id']
        keyboard.add(InlineKeyboardButton(name, callback_data=f"cat_edit:{cat_id}"))

    return keyboard

def open_cats_for_edit_pod_cat():
    keyboard = InlineKeyboardMarkup()

    for category in get_all_categories():
        name = category['name']
        cat_id = category['id']
        keyboard.add(InlineKeyboardButton(name, callback_data=f"pods_cat_edit:{cat_id}"))

    keyboard.add(InlineKeyboardButton(back, callback_data=f"pr_edit"))

    return keyboard

def open_pod_cats_for_edit(cat_id):
    keyboard = InlineKeyboardMarkup()

    for pod_category in get_pod_categories(cat_id):
        name = pod_category['name']
        pod_cat_id = pod_category['id']
        keyboard.add(InlineKeyboardButton(name, callback_data=f"podss_cat_edit:{pod_cat_id}"))

    return keyboard

def open_cats_for_add_pod_cat():
    keyboard = InlineKeyboardMarkup()

    for category in get_all_categories():
        name = category['name']
        cat_id = category['id']
        keyboard.add(InlineKeyboardButton(name, callback_data=f"add_pod_cat_cat:{cat_id}"))

    keyboard.add(InlineKeyboardButton(back, callback_data=f"pr_edit"))

    return keyboard

def edit_cat_inl(cat_id):
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton(f"Изменить название", callback_data=f"edit_cat_name:{cat_id}"))
    kb.append(InlineKeyboardButton(f"Удалить", callback_data=f"del_cat:{cat_id}"))
    kb.append(InlineKeyboardButton(back, callback_data=f"edit_cat"))

    keyboard.add(kb[0], kb[1])
    keyboard.add(kb[2])

    return keyboard

def choose_del_cat(cat_id):
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton(f"✅ Да, хочу", callback_data=f"dels_cat:yes:{cat_id}"))
    kb.append(InlineKeyboardButton(f"❌ Нет, не хочу", callback_data=f"dels_cat:no:{cat_id}"))

    keyboard.add(kb[0], kb[1])

    return keyboard

def choose_del_all_cats():
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton(f"✅ Да, хочу", callback_data=f"dels_all_cat:yes"))
    kb.append(InlineKeyboardButton(f"❌ Нет, не хочу", callback_data=f"dels_all_cat:no"))

    keyboard.add(kb[0], kb[1])

    return keyboard

def update_pod_cat_inl(pod_cat_id):
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton(f"Изменить название", callback_data=f"edit_pod_cat_name:{pod_cat_id}"))
    kb.append(InlineKeyboardButton(f"Удалить", callback_data=f"del_pod_cat:{pod_cat_id}"))
    kb.append(InlineKeyboardButton(back, callback_data=f"edit_pod_cat"))

    keyboard.add(kb[0], kb[1])
    keyboard.add(kb[2])

    return keyboard

def choose_del_pod_cat(pod_cat_id):
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton(f"✅ Да, хочу", callback_data=f"dels_pod_cat:yes:{pod_cat_id}"))
    kb.append(InlineKeyboardButton(f"❌ Нет, не хочу", callback_data=f"dels_pod_cat:no:{pod_cat_id}"))

    keyboard.add(kb[0], kb[1])

    return keyboard

def choose_del_all_pod_cats():
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton(f"✅ Да, хочу", callback_data=f"dels_all_pod_cats:yes"))
    kb.append(InlineKeyboardButton(f"❌ Нет, не хочу", callback_data=f"dels_all_pod_cats:no"))

    keyboard.add(kb[0], kb[1])

    return keyboard

def open_cats_for_add_pos():
    keyboard = InlineKeyboardMarkup()

    for category in get_all_categories():
        name = category['name']
        cat_id = category['id']
        keyboard.add(InlineKeyboardButton(name, callback_data=f"add_pos_cat:{cat_id}"))

    keyboard.add(InlineKeyboardButton(back, callback_data=f"pr_edit"))

    return keyboard

def open_pod_cats_for_add_pos(cat_id):
    keyboard = InlineKeyboardMarkup()

    for pod_category in get_pod_categories(cat_id):
        name = pod_category['name']
        pod_cat_id = pod_category['id']
        keyboard.add(InlineKeyboardButton(name, callback_data=f"pod_cat_add_pos:{pod_cat_id}:{cat_id}"))

    keyboard.add(InlineKeyboardButton(f"💎 Выбрать эту категорию", callback_data=f"add_poss_cat:{cat_id}"))
    keyboard.add(InlineKeyboardButton(back, callback_data=f"add_pos"))

    return keyboard


def open_cats_for_edit_pos():
    keyboard = InlineKeyboardMarkup()

    for category in get_all_categories():
        name = category['name']
        cat_id = category['id']
        keyboard.add(InlineKeyboardButton(name, callback_data=f"edit_pos_cat:{cat_id}"))

    keyboard.add(InlineKeyboardButton(back, callback_data=f"pr_edit"))

    return keyboard

def open_pod_cats_for_edit_pos(cat_id):
    keyboard = InlineKeyboardMarkup()

    for pod_category in get_pod_categories(cat_id):
        name = pod_category['name']
        pod_cat_id = pod_category['id']
        keyboard.add(InlineKeyboardButton(name, callback_data=f"pod_cat_edit_pos:{pod_cat_id}:{cat_id}"))
    for position in get_positions(cat_id):
        name = position['name']
        pos_id = position['id']
        price = position['price']
        items = f"{len(get_items(position_id=pos_id))}шт"
        if position['infinity'] == "+":
            items = "[Безлимит]"
        if position['pod_category_id'] is not None:
            continue
        keyboard.add(InlineKeyboardButton(f"{name} | {price}₽ | {items}", callback_data=f"edit_pos:{pos_id}"))

    keyboard.add(InlineKeyboardButton(back, callback_data=f"edit_pos"))

    return keyboard

def open_positions_for_edit(cat_id, pod_cat_id = None):
    keyboard = InlineKeyboardMarkup()

    if pod_cat_id is None:
        for position in get_positions(cat_id):
            name = position['name']
            pos_id = position['id']
            price = position['price']
            items = get_items(position_id=pos_id)
            keyboard.add(InlineKeyboardButton(f"{name} | {price}₽ | {len(items)}шт.", callback_data=f"edit_pos:{pos_id}"))
    else:
        for position in get_positions(cat_id, pod_cat_id):
            name = position['name']
            pos_id = position['id']
            price = position['price']
            items = get_items(position_id=pos_id)
            keyboard.add(InlineKeyboardButton(f"{name} | {price}₽ | {len(items)}шт.", callback_data=f"edit_pos:{pos_id}"))

    keyboard.add(InlineKeyboardButton(back, callback_data=f"edit_pos"))

    return keyboard

def edit_pos_inl(pos_id):
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton(f"Цена", callback_data=f"edit_price_pos:{pos_id}"))
    kb.append(InlineKeyboardButton(f"Название", callback_data=f"edit_name_pos:{pos_id}"))
    kb.append(InlineKeyboardButton(f"Описание", callback_data=f"edit_desc_pos:{pos_id}"))
    kb.append(InlineKeyboardButton(f"Фото", callback_data=f"edit_photo_pos:{pos_id}"))
    kb.append(InlineKeyboardButton(f"Тип товара", callback_data=f"edit_infinity_pos:{pos_id}"))
    kb.append(InlineKeyboardButton(f"Удалить", callback_data=f"edit_del_pos:{pos_id}"))
    kb.append(InlineKeyboardButton(f"Очистить товары", callback_data=f"edit_clear_items_pos:{pos_id}"))
    kb.append(InlineKeyboardButton(f"Загрузить товары", callback_data=f"edit_upload_items_pos:{pos_id}"))


    keyboard.add(kb[0], kb[1])
    keyboard.add(kb[2], kb[3], kb[4])
    keyboard.add(kb[5])
    keyboard.add(kb[7], kb[6])
    keyboard.add(InlineKeyboardButton(back, callback_data=f"edit_pos"))

    return keyboard

def choose_del_pos(pos_id):
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton(f"✅ Да, хочу", callback_data=f"dels_pos:yes:{pos_id}"))
    kb.append(InlineKeyboardButton(f"❌ Нет, не хочу", callback_data=f"dels_pos:no:{pos_id}"))

    keyboard.add(kb[0], kb[1])

    return keyboard

def choose_del_all_pos():
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton(f"✅ Да, хочу", callback_data=f"dels_all_poss:yes"))
    kb.append(InlineKeyboardButton(f"❌ Нет, не хочу", callback_data=f"dels_all_poss:no"))

    keyboard.add(kb[0], kb[1])

    return keyboard

def open_cats_for_add_items():
    keyboard = InlineKeyboardMarkup()

    for category in get_all_categories():
        name = category['name']
        cat_id = category['id']
        keyboard.add(InlineKeyboardButton(name, callback_data=f"add_items_cat:{cat_id}"))

    keyboard.add(InlineKeyboardButton(back, callback_data=f"pr_edit"))

    return keyboard

def open_pod_cats_for_add_items(cat_id):
    keyboard = InlineKeyboardMarkup()

    for pod_category in get_pod_categories(cat_id):
        name = pod_category['name']
        pod_cat_id = pod_category['id']
        keyboard.add(InlineKeyboardButton(name, callback_data=f"pod_cat_add_items:{pod_cat_id}:{cat_id}"))
    for position in get_positions(cat_id):
        name = position['name']
        pos_id = position['id']
        price = position['price']
        items = f"{len(get_items(position_id=pos_id))}шт"
        if position['infinity'] == "+":
            items = "[Безлимит]"
        if position['pod_category_id'] is not None:
            continue
        keyboard.add(InlineKeyboardButton(f"{name} | {price}₽ | {items}", callback_data=f"pos_add_items:{pos_id}"))

    keyboard.add(InlineKeyboardButton(back, callback_data=f"edit_pos"))

    return keyboard

def open_positions_for_add_items(cat_id, pod_cat_id = None):
    keyboard = InlineKeyboardMarkup()

    if pod_cat_id is None:
        for position in get_positions(cat_id):
            name = position['name']
            pos_id = position['id']
            price = position['price']
            items = get_items(position_id=pos_id)
            keyboard.add(InlineKeyboardButton(f"{name} | {price}₽ | {len(items)}шт.", callback_data=f"spos_add_items:{pos_id}"))
    else:
        for position in get_positions(cat_id, pod_cat_id):
            name = position['name']
            pos_id = position['id']
            price = position['price']
            items = get_items(position_id=pos_id)
            keyboard.add(InlineKeyboardButton(f"{name} | {price}₽ | {len(items)}шт.", callback_data=f"spos_add_items:{pos_id}"))

    keyboard.add(InlineKeyboardButton(back, callback_data=f"edit_pos"))

    return keyboard

def stop_add_items():
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton(f"❌ Закончить загрузку", callback_data=f"stop_add_items"))

    return keyboard

def choose_del_all_items():
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton(f"✅ Да, хочу", callback_data=f"dels_all_items:yes"))
    kb.append(InlineKeyboardButton(f"❌ Нет, не хочу", callback_data=f"dels_all_items:no"))

    keyboard.add(kb[0], kb[1])

    return keyboard

def choose_clear_items_pos(pos_id):
    keyboard = InlineKeyboardMarkup()
    kb = []

    kb.append(InlineKeyboardButton(f"✅ Да, хочу", callback_data=f"clear_items:yes:{pos_id}"))
    kb.append(InlineKeyboardButton(f"❌ Нет, не хочу", callback_data=f"clear_items:no:{pos_id}"))

    keyboard.add(kb[0], kb[1])

    return keyboard

# Упрощенные клавиатуры для товаров
def add_product_inl():
    """Клавиатура выбора типа товара"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="♾️ Бесконечный", callback_data="set_infinity:True")],
        [InlineKeyboardButton(text="📦 Обычный", callback_data="set_infinity:False")],
        [InlineKeyboardButton(text=back, callback_data="pr_edit")]
    ])
    return keyboard

def edit_product_inl():
    """Клавиатура со списком товаров для редактирования"""
    kb = []
    positions = get_positions_simple()
    
    for position in positions:
        name = position['name']
        pos_id = position['id']
        price = position['price']
        items_count = len(get_items_simple(pos_id))
        
        if position['infinity'] == "+":
            items_display = "♾️"
        else:
            items_display = f"{items_count}шт"
            
        kb.append([InlineKeyboardButton(
            text=f"{name} | ${price} | {items_display}", 
            callback_data=f"edit_pos:{pos_id}"
        )])
    
    kb.append([InlineKeyboardButton(text=back, callback_data="pr_edit")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard

def product_edit_menu(pos_id):
    """Меню редактирования конкретного товара"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📝 Название", callback_data=f"edit_pos_name:{pos_id}"),
            InlineKeyboardButton(text="📄 Описание", callback_data=f"edit_pos_desc:{pos_id}")
        ],
        [
            InlineKeyboardButton(text="💰 Цена", callback_data=f"edit_pos_price:{pos_id}"),
            InlineKeyboardButton(text="📦 Товары", callback_data=f"edit_pos_items:{pos_id}")
        ],
        [InlineKeyboardButton(text="🗑 Удалить", callback_data=f"delete_pos:{pos_id}")],
        [InlineKeyboardButton(text=back, callback_data="edit_products")]
    ])
    return keyboard

def confirm_delete_product(pos_id):
    """Подтверждение удаления товара"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Да, удалить", callback_data=f"confirm_delete_pos:{pos_id}"),
            InlineKeyboardButton(text="❌ Отмена", callback_data=f"edit_pos:{pos_id}")
        ]
    ])
    return keyboard