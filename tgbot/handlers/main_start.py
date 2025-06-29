# - *- coding: utf- 8 - *-
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import CommandStart, Command
from tgbot.keyboards.inline_user import sub, user_menu, back_to_profile, profile_inl, back_to_user_menu, chat_inl, news_inl, faq_inl, support_inll, language_selection, language_selection_with_back
from tgbot.services.sqlite import get_user, get_settings, update_user, last_purchases, get_activate_coupon, get_coupon_search, \
delete_coupon, update_coupon, add_activ_coupon, activate_coupon, register_user
from tgbot.data.loader import bot
from tgbot.utils.other_functions import open_profile, convert_ref
from tgbot.utils.utils_functions import get_admins, get_date
from tgbot.utils.translations import get_text, get_user_language
from contextlib import suppress
from tgbot.filters.is_buy import IsBuy
from tgbot.filters.is_ban import IsBan
from tgbot.filters.is_work import IsWork
from tgbot.filters.is_refill import IsRefill
from tgbot.filters.is_sub import IsSub
from tgbot.filters.is_admin import IsAdmin
from aiogram.exceptions import TelegramBadRequest

# Создаём роутер для этого модуля
router = Router()

# Определяем состояния
class CouponStates(StatesGroup):
    set_coupon = State()

# Команды для входа в админ-панель
@router.message(IsAdmin(), Command(commands=['admin', 'adm', 'a']))
async def admin_menu_command(message: Message, state: FSMContext):
    await state.clear()
    from tgbot.keyboards.inline_admin import admin_menu
    lang = get_user_language(message.from_user.id)
    await message.answer(get_text(lang, 'admin_welcome'), reply_markup=admin_menu())

@router.message(IsBan())
async def is_ban_message(message: Message, state: FSMContext):
    await state.clear()
    lang = get_user_language(message.from_user.id)
    await message.answer(get_text(lang, 'banned'))

@router.callback_query(IsBan())
async def is_ban_callback(call: CallbackQuery, state: FSMContext):
    await state.clear()
    lang = get_user_language(call.from_user.id)
    await call.answer(get_text(lang, 'banned'))

@router.message(IsWork())
async def is_work_message(message: Message, state: FSMContext):
    await state.clear()
    lang = get_user_language(message.from_user.id)
    await message.answer(get_text(lang, 'maintenance'))

@router.callback_query(IsWork())
async def is_work_callback(call: CallbackQuery, state: FSMContext):
    await state.clear()
    lang = get_user_language(call.from_user.id)
    await call.answer(get_text(lang, 'maintenance'))

@router.callback_query(IsRefill(), F.data == "refill")
async def is_refill(call: CallbackQuery, state: FSMContext):
    await state.clear()
    lang = get_user_language(call.from_user.id)
    await call.answer(get_text(lang, 'refill_disabled'), show_alert=True)

@router.callback_query(IsSub())
async def is_subs_callback(call: CallbackQuery, state: FSMContext):
    await state.clear()
    lang = get_user_language(call.from_user.id)
    await call.message.answer(get_text(lang, 'not_subscribed'), reply_markup=sub())

@router.message(IsSub())
async def is_subs_message(msg: Message, state: FSMContext):
    await state.clear()
    lang = get_user_language(msg.from_user.id)
    await msg.answer(get_text(lang, 'not_subscribed'), reply_markup=sub())

@router.callback_query(F.data == 'subprov')
async def sub_prov(call: CallbackQuery, state: FSMContext):
    await state.clear()
    if call.message.chat.type == 'private':
        user = get_user(id=call.from_user.id)
        lang = get_user_language(call.from_user.id)
        kb = user_menu(call.from_user.id)
        welcome_msg = get_text(lang, 'welcome_msg', user_name=user['user_name'])
        
        # Используем пустое фото, так как start_photo больше не доступно
        await call.message.answer(welcome_msg, reply_markup=kb)

#####################################################################################
#####################################################################################
#####################################################################################
    
@router.message(CommandStart())
async def main_start(message: Message, state: FSMContext):
    await state.clear()
    user = get_user(id=message.from_user.id)
    
    # Если пользователь новый, показываем выбор языка
    if user is None:
        choose_msg = get_text('ru', 'choose_language')  # По умолчанию русский для выбора
        await message.answer(choose_msg, reply_markup=language_selection())
        return
    
    # Получаем язык пользователя
    lang = get_user_language(message.from_user.id)
    kb = user_menu(message.from_user.id)
    welcome_msg = get_text(lang, 'welcome_msg', user_name=user['user_name'])

    if get_settings()['is_ref'] == 'True':
        args = message.text.split()[1:] if len(message.text.split()) > 1 else []
        ref_id = args[0] if args else ""

        if ref_id == "":
            await message.answer(welcome_msg, reply_markup=kb)
        else:
            try:
                ref_id_int = int(ref_id)
                if get_user(id=ref_id_int) is None:
                    await message.answer(welcome_msg, reply_markup=kb)
                else:
                    if user['ref_id'] is not None:
                        lang = get_user_language(message.from_user.id)
                        await message.answer(get_text(lang, 'has_referrer'))
                    else:
                        reffer = get_user(id=ref_id_int)
                        if reffer['id'] == message.from_user.id:
                            lang = get_user_language(message.from_user.id)
                            await message.answer(get_text(lang, 'cant_invite_self'))
                        else:
                            user_ref_count = reffer['ref_count']
                            reffer_lang = get_user_language(reffer['id'])
                            msg = get_text(reffer_lang, 'new_referral', user_name=user['user_name'], user_ref_count=user_ref_count + 1, convert_ref=convert_ref(user_ref_count + 1))

                            update_user(message.from_user.id, ref_id=reffer['id'], ref_user_name=reffer['user_name'], ref_first_name=reffer['first_name'])
                            update_user(reffer['id'], ref_count = user_ref_count + 1)

                            await bot.send_message(chat_id=reffer['id'], text=msg)

                            if reffer['ref_count'] + 1 == get_settings()['ref_lvl_1']:
                                remain_refs = get_settings()['ref_lvl_2'] - (reffer['ref_count'] + 1)
                                text = get_text(reffer_lang, 'new_ref_level', new_lvl=1, next_lvl=2, remain_refs=remain_refs, convert_ref=convert_ref(remain_refs))
                                await bot.send_message(chat_id=reffer['id'], text=text)
                                update_user(reffer['id'], ref_lvl=1)
                            elif reffer['ref_count'] + 1 == get_settings()['ref_lvl_2']:
                                remain_refs = get_settings()['ref_lvl_3'] - (reffer['ref_count'] + 1)
                                text = get_text(reffer_lang, 'new_ref_level', new_lvl=2, next_lvl=3, remain_refs=remain_refs, convert_ref=convert_ref(remain_refs))
                                await bot.send_message(chat_id=reffer['id'], text=text)
                                update_user(reffer['id'], ref_lvl=2)
                            elif reffer['ref_count'] + 1 == get_settings()['ref_lvl_3']:
                                text = get_text(reffer_lang, 'max_ref_level')
                                await bot.send_message(chat_id=reffer['id'], text=text)
                                update_user(reffer['id'], ref_lvl=3)

                            await message.answer(welcome_msg, reply_markup=kb)
            except ValueError:
                await message.answer(welcome_msg, reply_markup=kb)
    else:
        await message.answer(welcome_msg, reply_markup=kb)

@router.callback_query(F.data == "ref_system")
async def ref_systemm(call: CallbackQuery, state: FSMContext):
    await state.clear()
    status = get_settings()['is_ref']
    bott = await bot.get_me()
    bot_name = bott.username
    ref_link = f"<code>https://t.me/{bot_name}?start={call.from_user.id}</code>"
    user = get_user(id=call.from_user.id)
    ref_earn = user['ref_earn']
    ref_count = user['ref_count']
    ref_lvl = user['ref_lvl']
    lang = get_user_language(call.from_user.id)
    
    if ref_lvl == 0:
        lvl = 1
        ref_percent = get_settings()['ref_percent_1']
    if ref_lvl == 1:
        lvl = 2
        ref_percent = get_settings()['ref_percent_1']
    elif ref_lvl == 2:
        lvl = 3
        ref_percent = get_settings()['ref_percent_2']
    elif ref_lvl == 3:
        lvl = 3
        ref_percent = get_settings()['ref_percent_3']

    remain_refs = get_settings()[f'ref_lvl_{lvl}'] - user['ref_count']

    if ref_lvl == 3:
        mss = get_text(lang, 'current_max_level')
    else:
        mss = get_text(lang, 'next_level_remain', remain_refs=remain_refs)

    reffer_name = user['ref_first_name']
    if reffer_name is None:
        reffer = '<code>Никто</code>'
    else:
        reffer = f"<a href='tg://user?id={user['ref_id']}'>{reffer_name}</a>"

    # Используем многоязычный текст реферальной системы
    msg = f"""<b>💎 Реферальная система:
🔗 Ваша реф. ссылка: {ref_link}
📊 Ваш процент: {ref_percent}%
👤 Пригласивший: {reffer}
💰 Заработано: {ref_earn} USD
👥 Рефералов: {ref_count} {convert_ref(ref_count)}
🏆 Уровень: {ref_lvl}
{mss}</b>"""

    if status == "True":
        await call.message.edit_text(msg, reply_markup=back_to_profile(call.from_user.id))
    else:
        await call.answer(get_text(lang, 'ref_disabled'), show_alert=True)


# Просмотр истории покупок
@router.callback_query(F.data == "last_purchases")
async def user_history(call: CallbackQuery, state: FSMContext):
    purchasess = last_purchases(call.from_user.id, 10)
    lang = get_user_language(call.from_user.id)

    if len(purchasess) >= 1:
        await call.answer(get_text(lang, 'last_10_purchases'))
        with suppress(TelegramBadRequest):
            await call.message.delete()
            for purchases in purchasess:
                link_items = purchases['item']
                msg = get_text(lang, 'purchase_receipt', receipt=purchases['receipt'], name=purchases['position_name'], count=purchases['count'], price=purchases['price'], date=purchases['date'], link_items=link_items)
            await call.message.answer(msg)

        msg = open_profile(call.from_user.id)
        await call.message.answer(msg, reply_markup=profile_inl(call.from_user.id))
    else:
        await call.answer(get_text(lang, 'no_purchases'), show_alert=True)


@router.callback_query(F.data.startswith("promo_act"))
async def promo_activate_handler(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(CouponStates.set_coupon)
    lang = get_user_language(call.from_user.id)
    await call.message.edit_text(get_text(lang, 'promo_activate'), reply_markup=back_to_profile(call.from_user.id))

@router.message(CouponStates.set_coupon)
async def functions_profile_get(message: Message, state: FSMContext):
    await state.clear()
    coupon = message.text
    lang = get_user_language(message.from_user.id)

    if get_coupon_search(coupon=coupon) is None:
        await message.answer(get_text(lang, 'promo_not_found', coupon=coupon), reply_markup=back_to_profile(message.from_user.id))
    else:
        cop = get_coupon_search(coupon=coupon)["coupon"]
        uses = get_coupon_search(coupon=coupon)["uses"]
        discount = get_coupon_search(coupon=coupon)["discount"]
        user_id = message.from_user.id
        user = get_user(id=user_id)
        if uses == 0:
            await message.answer(get_text(lang, 'promo_no_uses'), reply_markup=back_to_profile(message.from_user.id))
            delete_coupon(coupon=coupon)
        elif get_activate_coupon(user_id=user_id) is None:
            update_user(user_id, balance=user['balance'] + discount)
            update_coupon(coupon, uses=int(uses) - 1)
            add_activ_coupon(user_id)
            activate_coupon(user_id=user_id, coupon=coupon)
            await message.answer(get_text(lang, 'promo_activated', discount=discount), reply_markup=back_to_profile(message.from_user.id))
        elif get_activate_coupon(user_id=user_id)["coupon_name"] == cop:
            await message.answer(get_text(lang, 'promo_already_used'), reply_markup=back_to_profile(message.from_user.id))


@router.callback_query(F.data == "profile:open")
async def profile_open(call: CallbackQuery, state: FSMContext):
    await state.clear()

    msg = open_profile(call.from_user.id)
    await call.message.edit_text(msg, reply_markup=profile_inl(call.from_user.id))

@router.callback_query(F.data == "back_to_menu")
async def again_start(call: CallbackQuery, state: FSMContext):
    await state.clear()

    user = get_user(id=call.from_user.id)
    lang = get_user_language(call.from_user.id)
    kb = user_menu(call.from_user.id)
    welcome_msg = get_text(lang, 'welcome_msg', user_name=user['user_name'])
    
    await call.message.edit_text(welcome_msg, reply_markup=kb)

@router.callback_query(F.data == "close_text_mail")
async def close_text_mails(call: CallbackQuery, state: FSMContext):
    await state.clear()

    await call.message.delete()

@router.callback_query(F.data == "FAQ")
async def faq_open(call: CallbackQuery, state: FSMContext):
    await state.clear()
    lang = get_user_language(call.from_user.id)

    faq = get_settings()['faq']
    if faq == "None" or faq == "-":
        faq = get_text(lang, 'no_faq')
    news = get_settings()['news']
    chat = get_settings()['chat']

    if get_settings()['chat'] == "-":
        chat = None

    if get_settings()['news'] == "-":
        news = None

    if news is None and chat is None:
        kb = back_to_user_menu(call.from_user.id)
    if news is None and chat is not None:
        kb = chat_inl()
    if news is not None and chat is None:
        kb = news_inl()
    if news is not None and chat is not None:
        kb = faq_inl()

    await call.message.delete()
    await call.message.answer(faq, reply_markup=kb)

@router.callback_query(F.data == "support")
async def support_open(call: CallbackQuery, state: FSMContext):
    await state.clear()
    lang = get_user_language(call.from_user.id)

    get_support = get_settings()['support']
    if get_support == "None" or get_support == "-":
        msg = get_text(lang, 'no_support')
    else:
        msg = get_text(lang, 'contact_support')

    if get_support == "None" or get_support == "-":
        kb = back_to_user_menu(call.from_user.id)
    else: 
        kb = support_inll()

    await call.message.delete()
    await call.message.answer(msg, reply_markup=kb)

# Обработчик выбора языка при первом запуске
@router.callback_query(F.data.startswith("set_language:"))
async def set_language(call: CallbackQuery):
    language = call.data.split(":")[1]
    user_id = call.from_user.id
    
    # Проверяем, есть ли пользователь в базе
    user = get_user(id=user_id)
    if not user:
        # Регистрируем нового пользователя с выбранным языком
        register_user(
            id=user_id,
            user_name=call.from_user.username or "None",
            first_name=call.from_user.first_name or "User",
            language=language
        )
        # Подтверждаем изменение языка
        await call.answer(get_text(language, 'language_changed'))
        
        # Отправляем приветственное сообщение на выбранном языке (новый пользователь)
        welcome_text = get_text(language, 'welcome_msg', user_name=call.from_user.username or call.from_user.first_name)
        await call.message.edit_text(welcome_text, reply_markup=user_menu(user_id))
    else:
        # Обновляем язык существующего пользователя
        update_user(user_id, language=language)
    
    # Подтверждаем изменение языка
    await call.answer(get_text(language, 'language_changed'))
    
    # Возвращаемся в профиль с обновленным языком
    msg = open_profile(user_id)
    await call.message.edit_text(msg, reply_markup=profile_inl(user_id))

# Обработчик изменения языка
@router.callback_query(F.data == "change_language")
async def change_language_handler(call: CallbackQuery):
    """Обработчик смены языка из профиля"""
    await call.message.edit_text(
        "🌐 Choose your language:\n🌐 Выберите ваш язык:",
        reply_markup=language_selection_with_back(call.from_user.id)
    )

# Обработчик возврата в главное меню из админки
@router.callback_query(F.data == "back_to_user_menu")
async def back_to_user_menu_handler(call: CallbackQuery):
    """Возврат в главное меню пользователя"""
    user_id = call.from_user.id
    lang = get_user_language(user_id)
    await call.message.edit_text(
        get_text(lang, 'main_menu'),
        reply_markup=user_menu(user_id)
    )

# Обработчик активации промокода через callback
@router.callback_query(F.data == "promocode")
async def promocode_handler(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(CouponStates.set_coupon)
    lang = get_user_language(call.from_user.id)
    await call.message.edit_text(get_text(lang, 'promo_activate'), reply_markup=back_to_profile(call.from_user.id))