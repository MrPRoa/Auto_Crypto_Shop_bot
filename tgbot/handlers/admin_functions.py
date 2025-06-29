# - *- coding: utf- 8 - *-
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.inline_admin import admin_menu, settings_inl, extra_settings_inl, on_off_inl, find_settings, payments_settings, set_back, back_sett, extra_back
from tgbot.keyboards.inline_user import user_menu
from tgbot.services.sqlite import get_user, get_settings, update_settings
from tgbot.filters.is_admin import IsAdmin
from tgbot.utils.translations import get_text, get_user_language

# Создаём роутер для этого модуля
router = Router()

# Определяем состояния FSM для админки
class AdminStates(StatesGroup):
    here_faq = State()
    here_support = State()
    here_chat = State()
    here_news = State()
    here_ref_percent = State()
    # Добавляем новые состояния
    mail_text = State()
    mail_photo_text = State()
    mail_photo = State()
    search_user = State()
    search_receipt = State()
    promo_name = State()
    promo_uses = State()
    promo_discount = State()
    promo_delete = State()
    ref_lvl_count = State()
    balance_add = State()
    balance_edit = State()
    send_message = State()

# Применяем фильтр администратора ко всем обработчикам в этом роутере
router.message.filter(IsAdmin())
router.callback_query.filter(IsAdmin())

@router.callback_query(F.data == "admin_menu")
async def admin_menu_callback(call: CallbackQuery, state: FSMContext):
    await state.clear()
    lang = get_user_language(call.from_user.id)
    await call.message.edit_text(get_text(lang, 'admin_welcome'), reply_markup=admin_menu())

@router.callback_query(F.data == "settings")
async def settings_menu(call: CallbackQuery):
    lang = get_user_language(call.from_user.id)
    await call.message.edit_text(get_text(lang, 'general_settings'), reply_markup=settings_inl())

# Обработчики для редактирования настроек
@router.callback_query(F.data == "faq:edit")
async def settings_set_faq(call: CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.here_faq)
    await call.message.edit_text(
        "<b>⚙️ Введите новый текст для FAQ\n"
        "❕ Вы можете использовать HTML разметку:\n"
        "❕ Отправьте <code>-</code> чтобы оставить пустым.</b>", 
        reply_markup=set_back()
    )

@router.callback_query(F.data.startswith("ref_percent:edit:"))
async def settings_set_ref_percent(call: CallbackQuery, state: FSMContext):
    lvl = call.data.split(":")[2]
    await state.update_data(cache_ref_lvl_to_edit_percent=lvl)
    await state.set_state(AdminStates.here_ref_percent)
    await call.message.edit_text(
        f"<b>⚙️ Введите новый процент для {lvl} реферального уровня:</b>", 
        reply_markup=set_back()
    )

@router.callback_query(F.data == "sup:edit")
async def settings_set_sup(call: CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.here_support)
    await call.message.edit_text(
        "<b>⚙️ Введите ссылку на пользователя (https://t.me/юзернейм)\n"
        "❕ Отправьте <code>-</code> чтобы оставить пустым.</b>", 
        reply_markup=set_back()
    )

@router.callback_query(F.data == "chat:edit")
async def settings_set_chat(call: CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.here_chat)
    await call.message.edit_text(
        "<b>⚙️ Отправьте ссылку на чат:\n"
        "❕ Отправьте <code>-</code> чтобы оставить пустым.</b>", 
        reply_markup=set_back()
    )

@router.callback_query(F.data == "news:edit")
async def settings_set_news(call: CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.here_news)
    await call.message.edit_text(
        "<b>⚙️ Отправьте ссылку на канал:\n"
        "❕ Отправьте <code>-</code> чтобы оставить пустым.</b>", 
        reply_markup=set_back()
    )

# Обработчики сообщений для установки настроек
@router.message(AdminStates.here_faq)
async def settings_faq_set(message: Message, state: FSMContext):
    await state.clear()
    update_settings(faq=message.text)
    await message.answer("<b>✅ Готово! FAQ было изменено!</b>", reply_markup=settings_inl())

@router.message(AdminStates.here_ref_percent)
async def settings_ref_per_set(message: Message, state: FSMContext):
    data = await state.get_data()
    lvl = data.get('cache_ref_lvl_to_edit_percent')
    await state.clear()

    if not message.text.isdigit():
        return await message.answer("<b>❌ Введите число!</b>")

    if lvl == "1":
        update_settings(ref_percent_1=int(message.text))
    elif lvl == "2":
        update_settings(ref_percent_2=int(message.text))
    elif lvl == "3":
        update_settings(ref_percent_3=int(message.text))
    
    await message.answer(f"<b>✅ Готово! Процент для {lvl} реферального уровня изменен!</b>", reply_markup=settings_inl())

@router.message(AdminStates.here_support)
async def settings_sup_set(message: Message, state: FSMContext):
    await state.clear()

    if message.text.startswith("https://t.me/") or message.text == "-":
        update_settings(support=message.text)
        await message.answer("<b>✅ Готово! Тех. Поддержка была изменена!</b>", reply_markup=settings_inl())
    else:
        await message.answer("<b>❌ Введите ссылку! (https://t.me/юзернейм)</b>")

@router.message(AdminStates.here_chat)
async def settings_chat_set(message: Message, state: FSMContext):
    await state.clear()

    if message.text.startswith("https://t.me/") or message.text == "-":
        update_settings(chat=message.text)
        await message.answer("<b>✅ Готово! Чат был изменен!</b>", reply_markup=settings_inl())
    else:
        await message.answer("<b>❌ Введите ссылку! (https://t.me/название_чата)</b>")

@router.message(AdminStates.here_news)
async def settings_news_set(message: Message, state: FSMContext):
    await state.clear()

    if message.text.startswith("https://t.me/") or message.text == "-":
        update_settings(news=message.text)
        await message.answer("<b>✅ Готово! Новостной канал был изменен!</b>", reply_markup=settings_inl())
    else:
        await message.answer("<b>❌ Введите ссылку! (https://t.me/название_канала)</b>")

@router.callback_query(F.data == "extra_settings")
async def extra_settings_menu(call: CallbackQuery):
    lang = get_user_language(call.from_user.id)
    await call.message.edit_text(get_text(lang, 'extra_settings'), reply_markup=extra_settings_inl())

@router.callback_query(F.data == "on_off")
async def on_off_menu(call: CallbackQuery):
    lang = get_user_language(call.from_user.id)
    await call.message.edit_text(get_text(lang, 'toggles'), reply_markup=on_off_inl())

@router.callback_query(F.data == "stats")
async def stats_menu(call: CallbackQuery):
    # Временная заглушка для статистики
    from tgbot.services.sqlite import all_users, all_purchases
    
    users = all_users()
    purchases = all_purchases()
    
    total_users = len(users)
    total_purchases = len(purchases)
    total_revenue = sum([p['price'] for p in purchases]) if purchases else 0
    
    lang = get_user_language(call.from_user.id)
    stats_text = get_text(lang, 'bot_stats', 
                         total_users=total_users,
                         total_purchases=total_purchases,
                         total_revenue=total_revenue)
    
    await call.message.edit_text(stats_text, reply_markup=back_sett())

@router.callback_query(F.data == "find:")
async def find_menu(call: CallbackQuery):
    lang = get_user_language(call.from_user.id)
    await call.message.edit_text(get_text(lang, 'search_menu'), reply_markup=find_settings())

@router.callback_query(F.data == "pr_edit")
async def products_edit_menu(call: CallbackQuery):
    from tgbot.keyboards.inline_admin import products_edits
    lang = get_user_language(call.from_user.id)
    await call.message.edit_text(get_text(lang, 'products_management'), reply_markup=products_edits())

@router.callback_query(F.data == "mail_start")
async def mail_start_menu(call: CallbackQuery):
    from tgbot.keyboards.inline_admin import mail_types
    lang = get_user_language(call.from_user.id)
    await call.message.edit_text(get_text(lang, 'mailing'), reply_markup=mail_types())

@router.callback_query(F.data == "payments")
async def payments_menu(call: CallbackQuery):
    lang = get_user_language(call.from_user.id)
    await call.message.edit_text(get_text(lang, 'payment_systems'), reply_markup=payments_settings())

@router.callback_query(F.data == "settings_back")
async def settings_back(call: CallbackQuery):
    lang = get_user_language(call.from_user.id)
    await call.message.edit_text(get_text(lang, 'admin_welcome'), reply_markup=admin_menu())

@router.callback_query(F.data == "set_back")
async def set_back_handler(call: CallbackQuery, state: FSMContext):
    await state.clear()
    lang = get_user_language(call.from_user.id)
    await call.message.edit_text(get_text(lang, 'general_settings'), reply_markup=settings_inl())

@router.callback_query(F.data.startswith("work:on_off"))
async def toggle_work(call: CallbackQuery):
    settings = get_settings()
    new_status = "False" if settings['is_work'] == "True" else "True"
    update_settings(is_work=new_status)
    
    lang = get_user_language(call.from_user.id)
    status = get_text(lang, 'bot_work_on') if new_status == "True" else get_text(lang, 'bot_work_off')
    await call.answer(get_text(lang, 'bot_work_status', status=status))
    await call.message.edit_reply_markup(reply_markup=on_off_inl())

@router.callback_query(F.data.startswith("buys:on_off"))
async def toggle_buys(call: CallbackQuery):
    settings = get_settings()
    new_status = "False" if settings['is_buy'] == "True" else "True"
    update_settings(is_buy=new_status)
    
    lang = get_user_language(call.from_user.id)
    status = get_text(lang, 'bot_work_on') if new_status == "True" else get_text(lang, 'bot_work_off')
    await call.answer(get_text(lang, 'buys_status', status=status))
    await call.message.edit_reply_markup(reply_markup=on_off_inl())

@router.callback_query(F.data.startswith("refills:on_off"))
async def toggle_refills(call: CallbackQuery):
    settings = get_settings()
    new_status = "False" if settings['is_refill'] == "True" else "True"
    update_settings(is_refill=new_status)
    
    lang = get_user_language(call.from_user.id)
    status = get_text(lang, 'bot_work_on') if new_status == "True" else get_text(lang, 'bot_work_off')
    await call.answer(get_text(lang, 'refills_status', status=status))
    await call.message.edit_reply_markup(reply_markup=on_off_inl())

@router.callback_query(F.data.startswith("ref:on_off"))
async def toggle_ref(call: CallbackQuery):
    settings = get_settings()
    new_status = "False" if settings['is_ref'] == "True" else "True"
    update_settings(is_ref=new_status)
    
    lang = get_user_language(call.from_user.id)
    status = get_text(lang, 'bot_work_on') if new_status == "True" else get_text(lang, 'bot_work_off')
    await call.answer(get_text(lang, 'ref_system_status', status=status))
    await call.message.edit_reply_markup(reply_markup=on_off_inl())

@router.callback_query(F.data.startswith("notify:on_off"))
async def toggle_notify(call: CallbackQuery):
    settings = get_settings()
    new_status = "False" if settings['is_notify'] == "True" else "True"
    update_settings(is_notify=new_status)
    
    lang = get_user_language(call.from_user.id)
    status = get_text(lang, 'bot_work_on') if new_status == "True" else get_text(lang, 'bot_work_off')
    await call.answer(get_text(lang, 'notifications_status', status=status))
    await call.message.edit_reply_markup(reply_markup=on_off_inl())

@router.callback_query(F.data.startswith("sub:on_off"))
async def toggle_sub(call: CallbackQuery):
    settings = get_settings()
    new_status = "False" if settings['is_sub'] == "True" else "True"
    update_settings(is_sub=new_status)
    
    lang = get_user_language(call.from_user.id)
    status = get_text(lang, 'bot_work_on') if new_status == "True" else get_text(lang, 'bot_work_off')
    await call.answer(get_text(lang, 'subscription_check_status', status=status))
    await call.message.edit_reply_markup(reply_markup=on_off_inl())

# Обработчики рассылки
@router.callback_query(F.data.startswith("mail:"))
async def mail_type_handler(call: CallbackQuery, state: FSMContext):
    mail_type = call.data.split(":")[1]
    await state.clear()
    
    lang = get_user_language(call.from_user.id)
    
    if mail_type == "text":
        await state.set_state(AdminStates.mail_text)
        await call.message.edit_text(get_text(lang, 'mail_text'), reply_markup=set_back())
    elif mail_type == "photo":
        await state.set_state(AdminStates.mail_photo_text)
        await call.message.edit_text(get_text(lang, 'mail_photo_text'), reply_markup=set_back())

@router.message(AdminStates.mail_text)
async def mail_text_handler(message: Message, state: FSMContext):
    await state.update_data(mail_text=message.text)
    lang = get_user_language(message.from_user.id)
    
    from tgbot.keyboards.inline_admin import opr_mail_text
    text = get_text(lang, 'confirm_mail', text=message.text)
    await message.answer(text, reply_markup=opr_mail_text())

@router.message(AdminStates.mail_photo_text)
async def mail_photo_text_handler(message: Message, state: FSMContext):
    await state.update_data(mail_text=message.text)
    await state.set_state(AdminStates.mail_photo)
    lang = get_user_language(message.from_user.id)
    await message.answer(get_text(lang, 'mail_photo'))

@router.message(AdminStates.mail_photo, F.content_type == "photo")
async def mail_photo_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(photo_id=message.photo[-1].file_id)
    lang = get_user_language(message.from_user.id)
    
    from tgbot.keyboards.inline_admin import opr_mail_photo
    text = get_text(lang, 'confirm_mail_photo', text=data['mail_text'])
    await message.answer_photo(
        photo=message.photo[-1].file_id,
        caption=text, 
        reply_markup=opr_mail_photo()
    )

@router.callback_query(F.data.startswith("mail_start_text:"))
async def confirm_mail_text(call: CallbackQuery, state: FSMContext):
    action = call.data.split(":")[1]
    lang = get_user_language(call.from_user.id)
    
    if action == "yes":
        data = await state.get_data()
        text = data['mail_text']
        
        # Отправляем рассылку
        from tgbot.services.sqlite import all_users
        from tgbot.data.loader import bot
        users = all_users()
        
        await call.message.edit_text(get_text(lang, 'mail_started'))
        
        success_count = 0
        for user in users:
            try:
                await bot.send_message(user['id'], text)
                success_count += 1
            except:
                pass
        
        await call.message.answer(f"✅ Рассылка завершена! Отправлено: {success_count}/{len(users)}")
    else:
        await call.message.edit_text(get_text(lang, 'mail_cancelled'))
    
    await state.clear()

@router.callback_query(F.data.startswith("mail_start_photo:"))
async def confirm_mail_photo(call: CallbackQuery, state: FSMContext):
    action = call.data.split(":")[1]
    lang = get_user_language(call.from_user.id)
    
    if action == "yes":
        data = await state.get_data()
        text = data['mail_text']
        photo_id = data['photo_id']
        
        # Отправляем рассылку
        from tgbot.services.sqlite import all_users
        from tgbot.data.loader import bot
        users = all_users()
        
        await call.message.edit_caption(get_text(lang, 'mail_started'))
        
        success_count = 0
        for user in users:
            try:
                await bot.send_photo(user['id'], photo_id, caption=text)
                success_count += 1
            except:
                pass
        
        await call.message.answer(f"✅ Рассылка завершена! Отправлено: {success_count}/{len(users)}")
    else:
        await call.message.edit_caption(get_text(lang, 'mail_cancelled'))
    
    await state.clear()

# Обработчики поиска
@router.callback_query(F.data == "find:profile")
async def search_profile_start(call: CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.search_user)
    lang = get_user_language(call.from_user.id)
    await call.message.edit_text(get_text(lang, 'enter_user_id'), reply_markup=set_back())

@router.message(AdminStates.search_user)
async def search_profile_finish(message: Message, state: FSMContext):
    await state.clear()
    user_input = message.text
    lang = get_user_language(message.from_user.id)
    
    # Поиск по ID или username
    user = None
    if user_input.startswith("@"):
        username = user_input[1:]
        # Поиск по username в базе данных
        from tgbot.services.sqlite import get_user_by_username
        user = get_user_by_username(username)
    else:
        try:
            user_id = int(user_input)
            user = get_user(id=user_id)
        except ValueError:
            pass
    
    if not user:
        await message.answer(get_text(lang, 'user_not_found'), reply_markup=find_settings())
        return
    
    ban_status = "Заблокирован" if user['is_ban'] == "True" else "Активен"
    username = user['user_name'] if user['user_name'] != "None" else "Отсутствует"
    
    text = get_text(lang, 'user_profile_admin',
                   user_id=user['id'],
                   first_name=user['first_name'],
                   username=username,
                   balance=user['balance'],
                   total_refill=user['total_refill'],
                   reg_date=user['reg_date'],
                   ref_count=user['ref_count'],
                   ban_status=ban_status)
    
    from tgbot.keyboards.inline_admin import profile_adm_inl
    await message.answer(text, reply_markup=profile_adm_inl(user['id']))

@router.callback_query(F.data == "find:receipt")
async def search_receipt_start(call: CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.search_receipt)
    lang = get_user_language(call.from_user.id)
    await call.message.edit_text(get_text(lang, 'enter_receipt'), reply_markup=set_back())

@router.message(AdminStates.search_receipt)
async def search_receipt_finish(message: Message, state: FSMContext):
    await state.clear()
    receipt = message.text
    lang = get_user_language(message.from_user.id)
    
    from tgbot.services.sqlite import get_purchase_by_receipt
    purchase = get_purchase_by_receipt(receipt)
    
    if not purchase:
        await message.answer(get_text(lang, 'receipt_not_found'), reply_markup=find_settings())
        return
    
    text = f"""
<b>🧾 Информация о чеке:</b>

🧾 Чек: <code>{purchase['receipt']}</code>
👤 Покупатель: <code>{purchase['first_name']}</code> (@{purchase['user_name']})
💎 Товар: <code>{purchase['position_name']}</code>
📦 Количество: <code>{purchase['count']}шт</code>
💰 Цена: <code>{purchase['price']}$</code>
📅 Дата: <code>{purchase['date']}</code>

📦 Товары:
<code>{purchase['item']}</code>
"""
    await message.answer(text, reply_markup=find_settings())

# Обработчики дополнительных настроек
@router.callback_query(F.data == "promo_create")
async def promo_create_start(call: CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.promo_name)
    lang = get_user_language(call.from_user.id)
    await call.message.edit_text("<b>❗ Введите название промокода</b>", reply_markup=extra_back())

@router.message(AdminStates.promo_name)
async def promo_name_handler(message: Message, state: FSMContext):
    await state.update_data(promo_name=message.text)
    await state.set_state(AdminStates.promo_uses)
    await message.answer("<b>❗ Введите количество использований</b>")

@router.message(AdminStates.promo_uses)
async def promo_uses_handler(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("<b>❌ Количество использований должно быть числом!</b>")
        return
    
    await state.update_data(promo_uses=int(message.text))
    await state.set_state(AdminStates.promo_discount)
    await message.answer("<b>❗ Введите скидку в долларах</b>")

@router.message(AdminStates.promo_discount)
async def promo_discount_handler(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("<b>❌ Скидка должна быть числом!</b>")
        return
    
    data = await state.get_data()
    discount = int(message.text)
    
    from tgbot.services.sqlite import create_coupon
    create_coupon(data['promo_name'], data['promo_uses'], discount)
    
    await state.clear()
    await message.answer(f"<b>✅ Промокод <code>{data['promo_name']}</code> создан!</b>", reply_markup=extra_settings_inl())

@router.callback_query(F.data == "promo_delete")
async def promo_delete_start(call: CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.promo_delete)
    await call.message.edit_text("<b>❗ Введите название промокода для удаления</b>", reply_markup=extra_back())

@router.message(AdminStates.promo_delete)
async def promo_delete_handler(message: Message, state: FSMContext):
    await state.clear()
    try:
        from tgbot.services.sqlite import delete_coupon
        delete_coupon(message.text)
        await message.answer(f"<b>✅ Промокод <code>{message.text}</code> удален!</b>", reply_markup=extra_settings_inl())
    except:
        await message.answer(f"<b>❌ Промокод <code>{message.text}</code> не найден!</b>", reply_markup=extra_settings_inl())

@router.callback_query(F.data.startswith("ref_lvl_edit:"))
async def ref_lvl_edit_start(call: CallbackQuery, state: FSMContext):
    lvl = call.data.split(":")[1]
    await state.update_data(ref_lvl=lvl)
    await state.set_state(AdminStates.ref_lvl_count)
    await call.message.edit_text(f"<b>❗ Введите количество рефералов для {lvl} уровня</b>", reply_markup=extra_back())

@router.message(AdminStates.ref_lvl_count)
async def ref_lvl_count_handler(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("<b>❌ Количество должно быть числом!</b>")
        return
    
    data = await state.get_data()
    lvl = data['ref_lvl']
    count = int(message.text)
    
    if lvl == "2":
        update_settings(ref_lvl_2=count)
    elif lvl == "3":
        update_settings(ref_lvl_3=count)
    
    await state.clear()
    await message.answer(f"<b>✅ Количество рефералов для {lvl} уровня изменено на {count}</b>", reply_markup=extra_settings_inl())

# Обработчики управления пользователями
@router.callback_query(F.data.startswith("user:balance_add:"))
async def balance_add_start(call: CallbackQuery, state: FSMContext):
    user_id = call.data.split(":")[2]
    await state.update_data(target_user_id=user_id)
    await state.set_state(AdminStates.balance_add)
    lang = get_user_language(call.from_user.id)
    await call.message.edit_text(get_text(lang, 'enter_balance_amount'), reply_markup=set_back())

@router.message(AdminStates.balance_add)
async def balance_add_finish(message: Message, state: FSMContext):
    try:
        amount = float(message.text.replace(',', '.'))
        data = await state.get_data()
        user_id = int(data['target_user_id'])
        
        user = get_user(id=user_id)
        new_balance = user['balance'] + amount
        
        from tgbot.services.sqlite import update_user
        update_user(user_id, balance=new_balance)
        
        await state.clear()
        lang = get_user_language(message.from_user.id)
        await message.answer(get_text(lang, 'balance_added'), reply_markup=find_settings())
        
    except ValueError:
        await message.answer("<b>❌ Сумма должна быть числом!</b>")

@router.callback_query(F.data.startswith("user:balance_edit:"))
async def balance_edit_start(call: CallbackQuery, state: FSMContext):
    user_id = call.data.split(":")[2]
    await state.update_data(target_user_id=user_id)
    await state.set_state(AdminStates.balance_edit)
    lang = get_user_language(call.from_user.id)
    await call.message.edit_text(get_text(lang, 'enter_new_balance'), reply_markup=set_back())

@router.message(AdminStates.balance_edit)
async def balance_edit_finish(message: Message, state: FSMContext):
    try:
        new_balance = float(message.text.replace(',', '.'))
        data = await state.get_data()
        user_id = int(data['target_user_id'])
        
        from tgbot.services.sqlite import update_user
        update_user(user_id, balance=new_balance)
        
        await state.clear()
        lang = get_user_language(message.from_user.id)
        await message.answer(get_text(lang, 'balance_updated'), reply_markup=find_settings())
        
    except ValueError:
        await message.answer("<b>❌ Баланс должен быть числом!</b>")

@router.callback_query(F.data.startswith("user:is_ban_ban:"))
async def ban_user(call: CallbackQuery):
    user_id = int(call.data.split(":")[3])
    user = get_user(id=user_id)
    
    from tgbot.services.sqlite import update_user
    update_user(user_id, is_ban="True")
    
    lang = get_user_language(call.from_user.id)
    await call.answer(get_text(lang, 'user_banned'))
    
    # Обновляем профиль
    ban_status = "Заблокирован"
    username = user['user_name'] if user['user_name'] != "None" else "Отсутствует"
    
    text = get_text(lang, 'user_profile_admin',
                   user_id=user['id'],
                   first_name=user['first_name'],
                   username=username,
                   balance=user['balance'],
                   total_refill=user['total_refill'],
                   reg_date=user['reg_date'],
                   ref_count=user['ref_count'],
                   ban_status=ban_status)
    
    from tgbot.keyboards.inline_admin import profile_adm_inl
    await call.message.edit_text(text, reply_markup=profile_adm_inl(user_id))

@router.callback_query(F.data.startswith("user:is_ban_unban:"))
async def unban_user(call: CallbackQuery):
    user_id = int(call.data.split(":")[3])
    user = get_user(id=user_id)
    
    from tgbot.services.sqlite import update_user
    update_user(user_id, is_ban="False")
    
    lang = get_user_language(call.from_user.id)
    await call.answer(get_text(lang, 'user_unbanned'))
    
    # Обновляем профиль
    ban_status = "Активен"
    username = user['user_name'] if user['user_name'] != "None" else "Отсутствует"
    
    text = get_text(lang, 'user_profile_admin',
                   user_id=user['id'],
                   first_name=user['first_name'],
                   username=username,
                   balance=user['balance'],
                   total_refill=user['total_refill'],
                   reg_date=user['reg_date'],
                   ref_count=user['ref_count'],
                   ban_status=ban_status)
    
    from tgbot.keyboards.inline_admin import profile_adm_inl
    await call.message.edit_text(text, reply_markup=profile_adm_inl(user_id))

@router.callback_query(F.data.startswith("user:sms:"))
async def send_message_start(call: CallbackQuery, state: FSMContext):
    user_id = call.data.split(":")[2]
    await state.update_data(target_user_id=user_id)
    await state.set_state(AdminStates.send_message)
    await call.message.edit_text("<b>📨 Введите сообщение для отправки:</b>", reply_markup=set_back())

@router.message(AdminStates.send_message)
async def send_message_finish(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = int(data['target_user_id'])
    
    try:
        from tgbot.data.loader import bot
        await bot.send_message(user_id, f"📨 Сообщение от администратора:\n\n{message.text}")
        await message.answer("✅ Сообщение отправлено!", reply_markup=find_settings())
    except:
        await message.answer("❌ Не удалось отправить сообщение!", reply_markup=find_settings())
    
    await state.clear()

# Обработчик для возврата к дополнительным настройкам
@router.callback_query(F.data == "extra_settings_back")
async def extra_settings_back_handler(call: CallbackQuery, state: FSMContext):
    await state.clear()
    lang = get_user_language(call.from_user.id)
    await call.message.edit_text(get_text(lang, 'extra_settings'), reply_markup=extra_settings_inl())

# Добавляем недостающий обработчик для extra_settings
@router.callback_query(F.data == "extra_settings")
async def extra_settings_handler(call: CallbackQuery, state: FSMContext):
    await state.clear()
    lang = get_user_language(call.from_user.id)
    await call.message.edit_text(get_text(lang, 'extra_settings'), reply_markup=extra_settings_inl())

# Обработчик для возврата из поиска
@router.callback_query(F.data == "find:back") 
async def find_back_handler(call: CallbackQuery, state: FSMContext):
    await state.clear()
    lang = get_user_language(call.from_user.id)
    await call.message.edit_text(get_text(lang, 'search_menu'), reply_markup=find_settings())

# TODO: Добавить остальные обработчики админки после основной миграции 