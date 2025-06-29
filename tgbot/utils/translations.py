# - *- coding: utf- 8 - *-

def format_number(number):
    """Форматирует число для отображения через запятую"""
    return str(number).replace('.', ',')

# Переводы для многоязычности бота
TRANSLATIONS = {
    'ru': {
        # Стартовые сообщения
        'welcome_msg': """
Добро пожаловать @{user_name}! Спасибо что пользуетесь нашим Магазином
Главное меню:
""",
        'choose_language': "🌍 Выберите язык / Choose language:",
        'language_changed': "✅ Язык успешно изменен на русский!",
        'main_menu': "Главное меню:",
        
        # Кнопки меню
        'products': "🛍️ Купить",
        'profile': "👤 Профиль", 
        'refill': "💰 Пополнить баланс",
        'faq': "📌 FAQ",
        'support': "💎 Саппорт",
        'back': "⬅ Вернуться",
        'close': "❌ Скрыть",
        'language_btn': "🌍 Язык",
        
        # Профиль
        'ref_system': "💎 Реферальная система",
        'promocode': "💰 Активировать промокод", 
        'last_purchases': "⭐ Последние покупки",
        'profile_text': """
<b>👤 Ваш Профиль:
💎 Юзер: @{user_name}
🆔 ID: <code>{user_id}</code>
💰 Баланс: <code>{balance} USD</code>
💵 Всего пополнено: <code>{total_refill} USD</code>
📌 Дата регистрации: <code>{reg_date}</code>
👥 Рефералов: <code>{ref_count} чел</code></b>
""",
        
        # Платежи
        'yoomoney': "📌 ЮMoney", 
        'lava': "💰 Lava",
        'lzt': "💚 Lolz",
        'crystal': "💎 CrystalPay",
        'crypto_usdt': "В USDT BEP-20",
        'crypto_usdt_polygon': "В USDT Polygon",
        'crypto_usdt_erc20': "В USDT ERC-20",
        
        # Ошибки и уведомления
        'not_subscribed': "<b>❗ Ошибка!\nВы не подписались на канал.</b>",
        'buy_disabled': "❌ Покупки временно отключены!",
        'banned': "<b>❌ Вы были заблокированы в боте!</b>",
        'maintenance': "<b>❌ Бот находиться на тех. работах!</b>",
        'refill_disabled': "❌ Пополнения временно отключены!",
        'ref_disabled': "❗ Реферальная система отключена!",
        'no_spam': "<b>❗ Пожалуйста, не спамьте.</b>",
        'no_spam_alert': "❗ Пожалуйста, не спамьте.",
        
        # Реферальная система
        'has_referrer': "<b>❗ У вас уже есть рефер!</b>",
        'cant_invite_self': "<b>❗ Вы не можете пригласить себя</b>",
        'new_referral': "<b>💎 У вас новый реферал! @{user_name} \n⚙️ Теперь у вас <code>{user_ref_count}</code> {convert_ref}!</b>",
        'new_ref_level': "<b>💚 У вас новый реферальный уровень, {new_lvl}! До {next_lvl} уровня осталось {remain_refs} {convert_ref}</b>",
        'max_ref_level': "<b>💚 У вас новый реферальный уровень, 3! Максимальный уровень!</b>",
        'current_max_level': "💚 У вас максимальный уровень!",
        'next_level_remain': "💚 До следующего уровня осталось пригласить <code>{remain_refs} чел</code>",
        
        # Промокоды
        'promo_activate': "<b>📩 Для активации промокода напишите его название</b>\n<b>⚙️ Пример: promo2023</b>",
        'promo_not_found': "<b>❌ Промокода <code>{coupon}</code> не существует!</b>",
        'promo_no_uses': "<b>❌ Вы не успели активировать промокод!</b>",
        'promo_activated': "<b>✅ Вы успешно активировали промокод и получили <code>{discount} USD</code>!</b>",
        'promo_already_used': "<b>❌ Вы уже активировали данный промокод!</b>",
        
        # Покупки
        'last_10_purchases': "⚙️ Последние 10 покупок",
        'no_purchases': "❗ У вас отсутствуют покупки",
        'purchase_receipt': "<b>🧾 Чек: <code>{receipt}</code> \n💎 Товар: <code>{name} | {count}шт | {price} USD</code> \n🕰 Дата покупки: <code>{date}</code> \n💚 Товары: \n{link_items}</b>\n",
        'enter_quantity': "<b>❗ Введите кол-во товаров которое хотите купить:</b>",
        'confirm_buy_one': "<b>❓ Вы уверены что хотите купить <code>{name}</code> в кол-ве <code>1шт.</code>?</b>",
        'confirm_buy_many': "<b>❓ Вы уверены что хотите купить <code>{name}</code> в кол-ве <code>{amount}шт.</code>?</b>",
        'quantity_number': "<b>❗ Кол-во должно быть числом!</b>",
        'insufficient_balance': "❗ У вас недостаточно средств. Пополните баланс!",
        'product_changed': "<b>❗️ Товар который вы хотели купить закончился или изменился.</b>",
        'purchase_cancelled': "<b>❗ Вы отменили покупку товаров.</b>",
        'preparing_products': "Подготовка товаров...",
        'purchase_success': """
<b>✅ Вы успешно купили товар(ы)</b>

🧾 Чек: <code>{receipt}</code>
️💎 Товар: <code>{name} | {amount}шт | {amount_pay}$</code>
🎲 Дата: <code>{buy_time}</code>

📦 Ваши товары:
{items}
""",
        'edit_products_list': "<b>📦 Выберите товар для редактирования:</b>",
        'edit_product_menu': """
<b>📦 Редактирование товара:</b>

📝 Название: <code>{name}</code>
📄 Описание: <code>{description}</code>
💰 Цена: <code>{price}$</code>
📦 Товаров: <code>{items}</code>
""",
        'products_management': "<b>💎 Управление товарами</b>\n\nВыберите действие:",
        'enter_product_name': "<b>📝 Введите название товара:</b>",
        'enter_product_description': "<b>📄 Введите описание товара:</b>",
        'enter_product_price': "<b>💰 Введите цену товара (в долларах):</b>",
        'price_positive': "<b>❌ Цена должна быть больше 0!</b>",
        'price_number': "<b>❌ Цена должна быть числом!</b>",
        'product_type_choice': "<b>⚙️ Выберите тип товара:</b>",
        'enter_infinite_content': "<b>📝 Введите содержимое бесконечного товара:</b>",
        'enter_products_list': "<b>📝 Введите товары (каждый с новой строки):</b>",
        'infinite_type': "Бесконечный",
        'regular_type': "Обычный",
        'product_added': """
<b>✅ Товар успешно добавлен!</b>

📝 Название: <code>{name}</code>
📄 Описание: <code>{description}</code>
💰 Цена: <code>{price}$</code>
⚙️ Тип: <code>{type}</code>
📦 Количество: <code>{count}</code>
""",
        'no_products_found': "❌ Товары не найдены",
        'product_not_found': "❌ Товар не найден",
        'enter_new_product_name': "<b>📝 Введите новое название товара:</b>",
        'product_name_updated': "<b>✅ Название товара изменено на: <code>{name}</code></b>",
        'mailing': "<b>📌 Рассылка</b>\n\nВыберите тип рассылки:",
        'mail_text': "<b>📝 Введите текст для рассылки:</b>",
        'mail_photo_text': "<b>📝 Введите текст для рассылки с фото:</b>",
        'mail_photo': "<b>🖼 Отправьте фото для рассылки:</b>",
        'confirm_mail': """
<b>📌 Подтверждение рассылки</b>

<b>Текст:</b>
{text}

<b>Отправить всем пользователям?</b>
""",
        'confirm_mail_photo': """
<b>📌 Подтверждение рассылки с фото</b>

<b>Текст:</b>
{text}

<b>Отправить всем пользователям?</b>
""",
        'mail_started': "<b>📌 Рассылка запущена!</b>",
        'mail_cancelled': "<b>❌ Рассылка отменена!</b>",
        'search_menu': "<b>🔍 Поиск</b>\n\nВыберите тип поиска:",
        'enter_user_id': "<b>👤 Введите ID пользователя или @username:</b>",
        'user_not_found': "❌ Пользователь не найден",
        'enter_receipt': "<b>🧾 Введите номер чека:</b>",
        'receipt_not_found': "❌ Чек не найден",
        'user_profile_admin': """
<b>👤 Профиль пользователя:</b>

🆔 ID: <code>{user_id}</code>
📝 Имя: <code>{first_name}</code>
📱 Username: @{username}
💰 Баланс: <code>{balance}$</code>
💵 Всего пополнено: <code>{total_refill}$</code>
📅 Дата регистрации: <code>{reg_date}</code>
👥 Рефералов: <code>{ref_count}</code>
🚫 Статус: <code>{ban_status}</code>
""",
        'enter_balance_amount': "<b>💰 Введите сумму для выдачи:</b>",
        'balance_added': "<b>✅ Баланс успешно выдан!</b>",
        'enter_new_balance': "<b>💰 Введите новый баланс:</b>",
        'balance_updated': "<b>✅ Баланс успешно изменен!</b>",
        'user_banned': "<b>🚫 Пользователь заблокирован!</b>",
        'user_unbanned': "<b>✅ Пользователь разблокирован!</b>",
        
        # Переключатели статусов
        'bot_work_on': "✅ Включена",
        'bot_work_off': "❌ Выключена",
        'bot_work_status': "Работа бота: {status}",
        'buys_status': "Покупки: {status}",
        'refills_status': "Пополнения: {status}",
        'ref_system_status': "Реф. система: {status}",
        'notifications_status': "Уведомления: {status}",
        'subscription_check_status': "Проверка подписки: {status}",
        
        # Доп переводы для админки
        'extra_settings': "<b>🎲 Дополнительные настройки</b>\n\nВыберите действие:",
        'toggles': "<b>❗ Выключатели</b>\n\nУправление состоянием бота:",
        'payment_systems': "<b>💰 Платежные системы</b>\n\nНастройка платежных систем:",
        
        # Категории и товары
        'no_categories': "<b>К сожалению в данный момент нет категорий :(</b>",
        'available_categories': "<b>Доступные на данный момент категории:</b>",
        'current_category': "<b>Текущая категория: <code>{name}</code>:</b>",
        'current_subcategory': "<b>Текущая под-категория: <code>{name}</code></b>",
        'no_products': "<b>К сожалению в данный момент нет товаров :(</b>",
        'no_product': "К сожалению сейчас нет данного товара :(",
        
        # Пополнения
        'choose_payment': "<b>💰 Выбери способ пополнения:</b>",
        'enter_amount': "<b>💰 Введите сумму пополнения (От {min_amount}$ до {max_amount}$)</b>",
        'payment_not_found': "❌ Оплата не найдена",
        'amount_must_be_number': "<b>❗ Сумма пополнения должна быть числом!</b>",
        'amount_limits': "<b>❗ Сумма пополнения должна быть больше или равна <code>{min_amount} USD</code> но меньше или равна <code>{max_amount} USD</code></b>",
        'refill_success': "<b>⭐ Вы успешно пополнили баланс на сумму <code>{amount} USD</code>\n💎 Способ: <code>{way}</code>\n🧾 Чек: <code>{receipt}</code></b>",
        'refill_notification': "<b>💎 Ваш реферал {name} пополнил баланс на <code>{amount}$</code> и с этого вам зачислено <code>{ref_amount}$</code></b>",
        'refill_cancelled': "<b>❌ Пополнение отменено</b>",
        'min_amount_error': "❌ Минимальная сумма пополнения: $1",
        'max_amount_error': "❌ Максимальная сумма пополнения: $10,000",
        'unknown_payment_method': "❌ Неизвестный метод оплаты",
        'payment_check': "🔍 Проверяем платеж...",
        
        # Криптовалютные пополнения
        'crypto_payment_info': """
<b>₿ Пополнение USDT (BEP-20)</b>

💳 Адрес кошелька:
<code>{wallet_address}</code>

💰 Сумма к оплате: <code>{amount} USDT</code>
🌐 Сеть: <code>{network}</code>
📋 Контракт: <code>{contract}</code>

⚠️ <b>Важно!</b> Переводите точно <code>{amount} USDT</code> для автоматического зачисления средств.
💰 На баланс зачислится: <code>{credit_amount} USD</code>

⏰ Платеж будет проверяться в течение 1 часа.
""",
        'crypto_payment_info_polygon': """
<b>₿ Пополнение USDT (Polygon)</b>

💳 Адрес кошелька:
<code>{wallet_address}</code>

💰 Сумма к оплате: <code>{amount} USDT</code>
🌐 Сеть: <code>{network}</code>
📋 Контракт: <code>{contract}</code>

⚠️ <b>Важно!</b> Переводите точно <code>{amount} USDT</code> для автоматического зачисления средств.
💰 На баланс зачислится: <code>{credit_amount} USD</code>

⏰ Платеж будет проверяться в течение 1 часа.
""",
        'crypto_payment_info_erc20': """
<b>₿ Пополнение USDT (ERC-20)</b>

💳 Адрес кошелька:
<code>{wallet_address}</code>

💰 Сумма к оплате: <code>{amount} USDT</code>
🌐 Сеть: <code>{network}</code>
📋 Контракт: <code>{contract}</code>

⚠️ <b>Важно!</b> Переводите точно <code>{amount} USDT</code> для автоматического зачисления средств.
💰 На баланс зачислится: <code>{credit_amount} USD</code>

⏰ Платеж будет проверяться в течение 1 часа.
""",
        'crypto_checking': "🔍 Проверяем поступление платежа...",
        'crypto_success': "<b>✅ Платеж получен!</b>\n💰 Баланс пополнен на <code>{amount} USD</code>",
        'crypto_timeout': "⏰ Время ожидания платежа истекло. Попробуйте снова.",
        'crypto_unavailable': "❌ Криптоплатежи временно недоступны",
        'crypto_config_error': "❌ Ошибка конфигурации криптоплатежей. Обратитесь к администратору.",
        'crypto_private_key_invalid': "❌ Неверный формат приватного ключа для сети {network}",
        'crypto_private_key_missing': "❌ Приватный ключ для сети {network} не настроен",
        'crypto_instructions': """💰 Пополнение через USDT BEP-20

💰 Сумма к переводу: ${amount} USDT
🌐 Сеть: BEP-20 (Binance Smart Chain)
💳 Адрес кошелька:

`{wallet_address}`

⚠️ ВАЖНО:
• Переводите ТОЧНО ${amount} USDT
• Используйте только сеть BEP-20 (BSC)  
• Другие сети не поддерживаются!
• У вас есть 1 час на отправку

🔍 После отправки нажмите "Проверить платеж"
""",
        'crypto_instructions_polygon': """💰 Пополнение через USDT Polygon

💰 Сумма к переводу: ${amount} USDT
🌐 Сеть: Polygon (MATIC)
💳 Адрес кошелька:

`{wallet_address}`

⚠️ ВАЖНО:
• Переводите ТОЧНО ${amount} USDT
• Используйте только сеть Polygon (MATIC)  
• Другие сети не поддерживаются!
• У вас есть 1 час на отправку

🔍 После отправки нажмите "Проверить платеж"
""",
        'crypto_instructions_erc20': """💰 Пополнение через USDT ERC-20

💰 Сумма к переводу: ${amount} USDT
🌐 Сеть: ERC-20 (Ethereum)
💳 Адрес кошелька:

`{wallet_address}`

⚠️ ВАЖНО:
• Переводите ТОЧНО ${amount} USDT
• Используйте только сеть ERC-20 (Ethereum)  
• Другие сети не поддерживаются!
• У вас есть 1 час на отправку

🔍 После отправки нажмите "Проверить платеж"
""",
        'crypto_payment_not_found': "❌ Данные о платеже не найдены. Создайте новый платеж.",
        'crypto_payment_expired': "⏰ Время ожидания платежа истекло (1 час)\n\n❌ Платеж отменен.",
        'crypto_checking_blockchain': "🔍 Проверяем блокчейн транзакции...",
        'crypto_payment_confirmed': """✅ Криптоплатеж подтвержден!

💰 Зачислено: ${amount} USDT
💳 Ваш баланс: ${new_balance}

Спасибо за пополнение!""",
        'crypto_check_error': "❌ Ошибка проверки: {error}\n\n🔄 Попробуйте позже",
        'crypto_transaction_not_found': "🔍 Транзакция не найдена\n\n💡 Убедитесь что:\n• Вы отправили точно ${amount} USDT\n• Использовали сеть BEP-20 (BSC){remaining_time}",
        'crypto_transaction_not_found_polygon': "🔍 Транзакция не найдена\n\n💡 Убедитесь что:\n• Вы отправили точно ${amount} USDT\n• Использовали сеть Polygon (MATIC){remaining_time}",
        'crypto_transaction_not_found_erc20': "🔍 Транзакция не найдена\n\n💡 Убедитесь что:\n• Вы отправили точно ${amount} USDT\n• Использовали сеть ERC-20 (Ethereum){remaining_time}",
        'crypto_checking_again': "🔍 Проверяем снова...",
        'crypto_waiting_cancelled': "❌ Ожидание платежа отменено",
        'crypto_payment_cancelled': "❌ Платеж отменен",
        'refill_cancelled_general': "❌ Пополнение отменено",
        
        # FAQ и поддержка
        'no_faq': "<b>⚙️ FAQ Не было настроено, обратитесь в поддержку!</b>",
        'no_support': "<b>⚙️ Владелец бота не оставил ссылку на Тех. Поддержку!</b>",
        'contact_support': "<b>📩 Чтобы обратиться в Тех. Поддержку нажмите на кнопку снизу:</b>",
        
        # Языки
        'russian': "🇷🇺 Русский",
        'english': "🇺🇸 English",
        
        # Новые переводы для покупок
        'choose_product': "🛍️ Выберите товар для покупки:",
        'product_out_of_stock': "❌ Товар закончился!",
        'product_info': """📦 <b>{name}</b>

📝 Описание: {description}
💰 Цена: ${price}
📊 В наличии: {items_count} шт.

Выберите количество для покупки:""",
        'not_enough_items': "❌ Недостаточно товара в наличии!",
        'invalid_quantity': "❌ Количество должно быть больше 0!",
        'quantity_processed': "✅ Количество обработано!",
        'quantity_must_be_number': "❌ Количество должно быть числом!",
        'cancel_buy': "❌ Отменить покупку",
        
        # Админские функции
        'admin_welcome': "⚙️ Добро пожаловать в меню Администратора",
        'general_settings': "🖤 Общие настройки",
        'bot_stats': """📊 Статистика бота

👥 Всего пользователей: {total_users}
🛒 Всего покупок: {total_purchases}
💰 Общая выручка: ${total_revenue}

📈 Подробная статистика будет добавлена позже""",
        'search_users': "🔍 Поиск пользователей",
        'search_products': "🔍 Поиск товаров",
        'search_purchases': "🔍 Поиск покупок",
        'enter_search_query': "🔍 Введите поисковый запрос:",
        'search_results': "🔍 Результаты поиска:",
        'no_search_results': "❌ По вашему запросу ничего не найдено",
        
        # Рассылка
        'mailing_menu': "📌 Меню рассылки",
        'enter_mailing_text': "📝 Введите текст рассылки:",
        'mailing_completed': "✅ Рассылка завершена!",
        'mailing_cancelled': "❌ Рассылка отменена!",
        
        # Платежные системы
        'payment_systems_menu': "💰 Управление платежными системами",
        'yoomoney_settings': "📌 Настройки ЮMoney",
        'lava_settings': "💰 Настройки Lava",
        'crystal_settings': "💎 Настройки CrystalPay",
        'crypto_settings': "₿ Настройки криптовалют",
        
        # Общие
        'confirm': "✅ Подтвердить",
        'cancel': "❌ Отменить",
        'back_to_menu': "⬅ Вернуться в меню",
        'settings_saved': "✅ Настройки сохранены!",
        'error_occurred': "❌ Произошла ошибка!",
        'operation_cancelled': "❌ Операция отменена!",
        'not_enough_permissions': "❌ Недостаточно прав!",
        'user_not_found': "❌ Пользователь не найден!",
        'invalid_input': "❌ Неверный ввод!",
        'success': "✅ Успешно!",
        'failed': "❌ Ошибка!",
    },
    
    'en': {
        # Стартовые сообщения
        'welcome_msg': """
Welcome @{user_name}! Thank you for using our Shop
Main menu:
""",
        'choose_language': "🌍 Выберите язык / Choose language:",
        'language_changed': "✅ Language successfully changed to English!",
        'main_menu': "Main menu:",
        
        # Кнопки меню
        'products': "🛍️ Buy",
        'profile': "👤 Profile",
        'refill': "💰 Add balance", 
        'faq': "📌 FAQ",
        'support': "💎 Support",
        'back': "⬅ Back",
        'close': "❌ Close",
        'language_btn': "🌍 Language",
        
        # Профиль
        'ref_system': "💎 Referral system",
        'promocode': "💰 Activate promo code",
        'last_purchases': "⭐ Recent purchases", 
        'profile_text': """
<b>👤 Your Profile:
💎 User: @{user_name}
🆔 ID: <code>{user_id}</code>
💰 Balance: <code>{balance} USD</code>
💵 Total refilled: <code>{total_refill} USD</code>
📌 Registration date: <code>{reg_date}</code>
👥 Referrals: <code>{ref_count} people</code></b>
""",
        
        # Платежи
        'yoomoney': "📌 YooMoney",
        'lava': "💰 Lava",
        'lzt': "💚 Lolz",
        'crystal': "💎 CrystalPay",
        'crypto_usdt': "In USDT BEP-20",
        'crypto_usdt_polygon': "In USDT Polygon",
        'crypto_usdt_erc20': "In USDT ERC-20",
        
        # Ошибки и уведомления
        'not_subscribed': "<b>❗ Error!\nYou haven't subscribed to the channel.</b>",
        'buy_disabled': "❌ Purchases temporarily disabled!",
        'banned': "<b>❌ You have been blocked in the bot!</b>", 
        'maintenance': "<b>❌ The bot is under maintenance!</b>",
        'refill_disabled': "❌ Refills temporarily disabled!",
        'ref_disabled': "❗ Referral system is disabled!",
        'no_spam': "<b>❗ Please don't spam.</b>",
        'no_spam_alert': "❗ Please don't spam.",
        
        # Реферальная система
        'has_referrer': "<b>❗ You already have a referrer!</b>",
        'cant_invite_self': "<b>❗ You cannot invite yourself</b>",
        'new_referral': "<b>💎 You have a new referral! @{user_name} \n⚙️ Now you have <code>{user_ref_count}</code> {convert_ref}!</b>",
        'new_ref_level': "<b>💚 You have a new referral level, {new_lvl}! {remain_refs} {convert_ref} left until level {next_lvl}</b>",
        'max_ref_level': "<b>💚 You have a new referral level, 3! Maximum level!</b>",
        'current_max_level': "💚 You have the maximum level!",
        'next_level_remain': "💚 {remain_refs} people left to invite for the next level",
        
        # Промокоды
        'promo_activate': "<b>📩 To activate a promo code, write its name</b>\n<b>⚙️ Example: promo2023</b>",
        'promo_not_found': "<b>❌ Promo code <code>{coupon}</code> doesn't exist!</b>",
        'promo_no_uses': "<b>❌ You didn't manage to activate the promo code!</b>",
        'promo_activated': "<b>✅ You successfully activated the promo code and received <code>{discount} USD</code>!</b>",
        'promo_already_used': "<b>❌ You have already activated this promo code!</b>",
        
        # Покупки
        'last_10_purchases': "⚙️ Last 10 purchases",
        'no_purchases': "❗ You have no purchases",
        'purchase_receipt': "<b>🧾 Receipt: <code>{receipt}</code> \n💎 Product: <code>{name} | {count}pcs | {price} USD</code> \n🕰 Purchase date: <code>{date}</code> \n💚 Items: \n{link_items}</b>\n",
        'enter_quantity': "<b>❗ Enter the quantity of products you want to buy:</b>",
        'confirm_buy_one': "<b>❓ Are you sure you want to buy <code>{name}</code> in quantity <code>1pc.</code>?</b>",
        'confirm_buy_many': "<b>❓ Are you sure you want to buy <code>{name}</code> in quantity <code>{amount}pcs.</code>?</b>",
        'quantity_number': "<b>❗ Quantity must be a number!</b>",
        'insufficient_balance': "❗ You don't have enough funds. Add balance!",
        'product_changed': "<b>❗️ The product you wanted to buy is out of stock or has changed.</b>",
        'purchase_cancelled': "<b>❗ You cancelled the purchase of products.</b>",
        'preparing_products': "Preparing products...",
        'purchase_success': """
<b>✅ You successfully bought product(s)</b>

🧾 Receipt: <code>{receipt}</code>
️💎 Product: <code>{name} | {amount}pcs | {amount_pay}$</code>
🎲 Date: <code>{buy_time}</code>

📦 Your items:
{items}
""",
        'edit_products_list': "<b>📦 Choose product to edit:</b>",
        'edit_product_menu': """
<b>📦 Product editing:</b>

📝 Name: <code>{name}</code>
📄 Description: <code>{description}</code>
💰 Price: <code>{price}$</code>
📦 Items: <code>{items}</code>
""",
        'products_management': "<b>💎 Products management</b>\n\nChoose action:",
        'enter_product_name': "<b>📝 Enter product name:</b>",
        'enter_product_description': "<b>📄 Enter product description:</b>",
        'enter_product_price': "<b>💰 Enter product price (in dollars):</b>",
        'price_positive': "<b>❌ Price must be greater than 0!</b>",
        'price_number': "<b>❌ Price must be a number!</b>",
        'product_type_choice': "<b>⚙️ Choose product type:</b>",
        'enter_infinite_content': "<b>📝 Enter infinite product content:</b>",
        'enter_products_list': "<b>📝 Enter products (each on a new line):</b>",
        'infinite_type': "Infinite",
        'regular_type': "Regular",
        'product_added': """
<b>✅ Product successfully added!</b>

📝 Name: <code>{name}</code>
📄 Description: <code>{description}</code>
💰 Price: <code>{price}$</code>
⚙️ Type: <code>{type}</code>
📦 Quantity: <code>{count}</code>
""",
        'no_products_found': "❌ Products not found",
        'product_not_found': "❌ Product not found",
        'enter_new_product_name': "<b>📝 Enter new product name:</b>",
        'product_name_updated': "<b>✅ Product name updated to: <code>{name}</code></b>",
        'mailing': "<b>📌 Mailing</b>\n\nChoose mailing type:",
        'mail_text': "<b>📝 Enter mailing text:</b>",
        'mail_photo_text': "<b>📝 Enter mailing text with photo:</b>",
        'mail_photo': "<b>🖼 Send photo for mailing:</b>",
        'confirm_mail': """
<b>📌 Mailing confirmation</b>

<b>Text:</b>
{text}

<b>Send to all users?</b>
""",
        'confirm_mail_photo': """
<b>📌 Mailing confirmation with photo</b>

<b>Text:</b>
{text}

<b>Send to all users?</b>
""",
        'mail_started': "<b>📌 Mailing started!</b>",
        'mail_cancelled': "<b>❌ Mailing cancelled!</b>",
        'search_menu': "<b>🔍 Search</b>\n\nChoose search type:",
        'enter_user_id': "<b>👤 Enter user ID or @username:</b>",
        'user_not_found': "❌ User not found",
        'enter_receipt': "<b>🧾 Enter receipt number:</b>",
        'receipt_not_found': "❌ Receipt not found",
        'user_profile_admin': """
<b>👤 User profile:</b>

🆔 ID: <code>{user_id}</code>
📝 Name: <code>{first_name}</code>
📱 Username: @{username}
💰 Balance: <code>{balance}$</code>
💵 Total refilled: <code>{total_refill}$</code>
📅 Registration date: <code>{reg_date}</code>
👥 Referrals: <code>{ref_count}</code>
🚫 Status: <code>{ban_status}</code>
""",
        'enter_balance_amount': "<b>💰 Enter amount to issue:</b>",
        'balance_added': "<b>✅ Balance successfully issued!</b>",
        'enter_new_balance': "<b>💰 Enter new balance:</b>",
        'balance_updated': "<b>✅ Balance successfully updated!</b>",
        'user_banned': "<b>🚫 User banned!</b>",
        'user_unbanned': "<b>✅ User unbanned!</b>",
        
        # Переключатели статусов
        'bot_work_on': "✅ Enabled",
        'bot_work_off': "❌ Disabled",
        'bot_work_status': "Bot status: {status}",
        'buys_status': "Buys: {status}",
        'refills_status': "Refills: {status}",
        'ref_system_status': "Ref. system: {status}",
        'notifications_status': "Notifications: {status}",
        'subscription_check_status': "Subscription check: {status}",
        
        # Доп переводы для админки
        'extra_settings': "<b>🎲 Additional settings</b>\n\nChoose action:",
        'toggles': "<b>❗ Toggles</b>\n\nBot status control:",
        'payment_systems': "<b>💰 Payment systems</b>\n\nPayment systems setup:",
        
        # Категории и товары
        'no_categories': "<b>Unfortunately there are no categories at the moment :(</b>",
        'available_categories': "<b>Available categories at the moment:</b>",
        'current_category': "<b>Current category: <code>{name}</code>:</b>",
        'current_subcategory': "<b>Current subcategory: <code>{name}</code></b>",
        'no_products': "<b>Unfortunately there are no products at the moment :(</b>",
        'no_product': "Unfortunately this product is not available now :(",
        
        # Пополнения
        'choose_payment': "<b>💰 Choose refill method:</b>",
        'enter_amount': "<b>💰 Enter refill amount (From {min_amount}$ to {max_amount}$)</b>",
        'payment_not_found': "❌ Payment not found",
        'amount_must_be_number': "<b>❗ Refill amount must be a number!</b>",
        'amount_limits': "<b>❗ Refill amount must be greater than or equal to <code>{min_amount} USD</code> but less than or equal to <code>{max_amount} USD</code></b>",
        'refill_success': "<b>⭐ You successfully refilled your balance by <code>{amount} USD</code>\n💎 Method: <code>{way}</code>\n🧾 Receipt: <code>{receipt}</code></b>",
        'refill_notification': "<b>💎 Your referral {name} refilled balance by <code>{amount}$</code> and you received <code>{ref_amount}$</code> from this</b>",
        'refill_cancelled': "<b>❌ Refill cancelled</b>",
        'min_amount_error': "❌ Minimum refill amount: $1",
        'max_amount_error': "❌ Maximum refill amount: $10,000",
        'unknown_payment_method': "❌ Unknown payment method",
        'payment_check': "🔍 Checking payment...",
        
        # Криптовалютные пополнения
        'crypto_payment_info': """
<b>₿ USDT Refill (BEP-20)</b>

💳 Wallet address:
<code>{wallet_address}</code>

💰 Amount to pay: <code>{amount} USDT</code>
🌐 Network: <code>{network}</code>
📋 Contract: <code>{contract}</code>

⚠️ <b>Important!</b> Transfer exactly <code>{amount} USDT</code> for automatic balance crediting.
💰 Balance will be credited: <code>{credit_amount} USD</code>

⏰ Payment will be checked within 1 hour.
""",
        'crypto_payment_info_polygon': """
<b>₿ USDT Refill (Polygon)</b>

💳 Wallet address:
<code>{wallet_address}</code>

💰 Amount to pay: <code>{amount} USDT</code>
🌐 Network: <code>{network}</code>
📋 Contract: <code>{contract}</code>

⚠️ <b>Important!</b> Transfer exactly <code>{amount} USDT</code> for automatic balance crediting.
💰 Balance will be credited: <code>{credit_amount} USD</code>

⏰ Payment will be checked within 1 hour.
""",
        'crypto_payment_info_erc20': """
<b>₿ USDT Refill (ERC-20)</b>

💳 Wallet address:
<code>{wallet_address}</code>

💰 Amount to pay: <code>{amount} USDT</code>
🌐 Network: <code>{network}</code>
📋 Contract: <code>{contract}</code>

⚠️ <b>Important!</b> Transfer exactly <code>{amount} USDT</code> for automatic balance crediting.
💰 Balance will be credited: <code>{credit_amount} USD</code>

⏰ Payment will be checked within 1 hour.
""",
        'crypto_checking': "🔍 Checking payment receipt...",
        'crypto_success': "<b>✅ Payment received!</b>\n💰 Balance refilled by <code>{amount} USD</code>",
        'crypto_timeout': "⏰ Payment waiting time expired. Try again.",
        'crypto_unavailable': "❌ Crypto payments temporarily unavailable",
        'crypto_config_error': "❌ Crypto payment configuration error. Contact administrator.",
        'crypto_private_key_invalid': "❌ Invalid private key format for network {network}",
        'crypto_private_key_missing': "❌ Private key for network {network} not configured",
        'crypto_instructions': """💰 Refill via USDT BEP-20

💰 Amount to transfer: ${amount} USDT
🌐 Network: BEP-20 (Binance Smart Chain)
💳 Wallet address:

`{wallet_address}`

⚠️ IMPORTANT:
• Transfer EXACTLY ${amount} USDT
• Use only BEP-20 network (BSC)  
• Other networks are not supported!
• You have 1 hour to send

🔍 After sending click "Check payment"
""",
        'crypto_instructions_polygon': """💰 Refill via USDT Polygon

💰 Amount to transfer: ${amount} USDT
🌐 Network: Polygon (MATIC)
💳 Wallet address:

`{wallet_address}`

⚠️ IMPORTANT:
• Transfer EXACTLY ${amount} USDT
• Use only Polygon network (MATIC)  
• Other networks are not supported!
• You have 1 hour to send

🔍 After sending click "Check payment"
""",
        'crypto_instructions_erc20': """💰 Refill via USDT ERC-20

💰 Amount to transfer: ${amount} USDT
🌐 Network: ERC-20 (Ethereum)
💳 Wallet address:

`{wallet_address}`

⚠️ IMPORTANT:
• Transfer EXACTLY ${amount} USDT
• Use only ERC-20 network (Ethereum)  
• Other networks are not supported!
• You have 1 hour to send

🔍 After sending click "Check payment"
""",
        'crypto_payment_not_found': "❌ Payment data not found. Create a new payment.",
        'crypto_payment_expired': "⏰ Payment waiting time expired (1 hour)\n\n❌ Payment cancelled.",
        'crypto_checking_blockchain': "🔍 Checking blockchain transactions...",
        'crypto_payment_confirmed': """✅ Crypto payment confirmed!

💰 Credited: ${amount} USDT
💳 Your balance: ${new_balance}

Thank you for the refill!""",
        'crypto_check_error': "❌ Check error: {error}\n\n🔄 Try later",
        'crypto_transaction_not_found': "🔍 Transaction not found\n\n💡 Make sure that:\n• You sent exactly ${amount} USDT\n• You used BEP-20 network (BSC){remaining_time}",
        'crypto_transaction_not_found_polygon': "🔍 Transaction not found\n\n💡 Make sure that:\n• You sent exactly ${amount} USDT\n• You used Polygon network (MATIC){remaining_time}",
        'crypto_transaction_not_found_erc20': "🔍 Transaction not found\n\n💡 Make sure that:\n• You sent exactly ${amount} USDT\n• You used ERC-20 network (Ethereum){remaining_time}",
        'crypto_checking_again': "🔍 Checking again...",
        'crypto_waiting_cancelled': "❌ Payment waiting cancelled",
        'crypto_payment_cancelled': "❌ Payment cancelled",
        'refill_cancelled_general': "❌ Refill cancelled",
        
        # FAQ и поддержка
        'no_faq': "<b>⚙️ FAQ was not configured, contact support!</b>",
        'no_support': "<b>⚙️ Bot owner didn't leave a link to Technical Support!</b>",
        'contact_support': "<b>📩 To contact Technical Support click the button below:</b>",
        
        # Языки
        'russian': "🇷🇺 Русский", 
        'english': "🇺🇸 English",
        
        # Новые переводы для покупок
        'choose_product': "🛍️ Choose product to buy:",
        'product_out_of_stock': "❌ Product is out of stock!",
        'product_info': """📦 <b>{name}</b>

📝 Description: {description}
💰 Price: ${price}
📊 In stock: {items_count} pcs.

Choose quantity to buy:""",
        'not_enough_items': "❌ Not enough items in stock!",
        'invalid_quantity': "❌ Quantity must be greater than 0!",
        'quantity_processed': "✅ Quantity processed!",
        'quantity_must_be_number': "❌ Quantity must be a number!",
        'cancel_buy': "❌ Cancel purchase",
        
        # Админские функции
        'admin_welcome': "⚙️ Welcome to Administrator menu",
        'general_settings': "🖤 General settings",
        'bot_stats': """📊 Bot statistics

👥 Total users: {total_users}
🛒 Total purchases: {total_purchases}
💰 Total revenue: ${total_revenue}

📈 Detailed statistics will be added later""",
        'search_users': "🔍 Search users",
        'search_products': "🔍 Search products",
        'search_purchases': "🔍 Search purchases",
        'enter_search_query': "🔍 Enter search query:",
        'search_results': "🔍 Search results:",
        'no_search_results': "❌ Nothing found for your query",
        
        # Рассылка
        'mailing_menu': "📌 Mailing menu",
        'enter_mailing_text': "📝 Enter mailing text:",
        'mailing_completed': "✅ Mailing completed!",
        'mailing_cancelled': "❌ Mailing cancelled!",
        
        # Платежные системы
        'payment_systems_menu': "💰 Payment systems management",
        'yoomoney_settings': "📌 YooMoney settings",
        'lava_settings': "💰 Lava settings",
        'crystal_settings': "💎 CrystalPay settings",
        'crypto_settings': "₿ Cryptocurrency settings",
        
        # Общие
        'confirm': "✅ Confirm",
        'cancel': "❌ Cancel",
        'back_to_menu': "⬅ Back to menu",
        'settings_saved': "✅ Settings saved!",
        'error_occurred': "❌ An error occurred!",
        'operation_cancelled': "❌ Operation cancelled!",
        'not_enough_permissions': "❌ Not enough permissions!",
        'user_not_found': "❌ User not found!",
        'invalid_input': "❌ Invalid input!",
        'success': "✅ Success!",
        'failed': "❌ Failed!",
    }
}

def get_text(user_language, key, **kwargs):
    """Получает текст на указанном языке с подстановкой параметров"""
    if user_language not in TRANSLATIONS:
        user_language = 'ru'  # По умолчанию русский
    
    text = TRANSLATIONS[user_language].get(key, f"Missing translation: {key}")
    
    # Подставляем параметры в текст
    if kwargs:
        try:
            text = text.format(**kwargs)
        except KeyError as e:
            print(f"Missing parameter in translation {key}: {e}")
    
    return text

def get_user_language(user_id):
    """Получает язык пользователя из базы данных"""
    from tgbot.services.sqlite import get_user
    
    user = get_user(id=user_id)
    if user and user.get('language'):
        return user['language']
    return 'ru'  # По умолчанию русский 