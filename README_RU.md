# 🛒 AutoCryptoShop - Telegram Bot

Современный телеграм-бот для автоматизированной торговли с поддержкой криптовалютных платежей и многоуровневой реферальной системой.

**[English Version](README_EN.md)**

## ✨ Особенности

- 🤖 **Современная архитектура** - построен на aiogram 3.20.0
- 💰 **Криптоплатежи** - поддержка USDT (BEP-20, Polygon, ERC-20)
- 🌍 **Многоязычность** - русский и английский языки
- 👥 **Реферальная система** - 3 уровня с настраиваемыми процентами
- 🎫 **Система промокодов** - гибкие скидки и бонусы
- 📊 **Админ-панель** - полное управление ботом
- 🔄 **Автоматизация** - планировщик задач и автобэкапы
- 📱 **Адаптивный интерфейс** - красивые inline-клавиатуры

## 🚀 Быстрый старт

### Требования

- Python 3.12+
- SQLite3
- Telegram Bot Token

### Установка

1. **Клонируйте репозиторий:**
```bash
git clone https://github.com/yourusername/AutoCryptoShop.git
cd AutoCryptoShop
```

2. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

3. **Настройте конфигурацию:**
Отредактируйте файл `settings.ini`:
```ini
[settings]
BOT_TOKEN = your_bot_token_here
ADMINS = your_admin_id_here
SUPPORT_USER = @your_support_username
CHAT_ID = your_chat_id
```

4. **Запустите бота:**
```bash
py -3.12 main.py
# или для Windows
start.bat
```

## 📋 Конфигурация

### settings.ini
```ini
[settings]
BOT_TOKEN = 1234567890:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
ADMINS = 123456789,987654321
SUPPORT_USER = @support_username
CHAT_ID = -1001234567890
CHANNEL_URL = https://t.me/yourchannel
FAQ = Часто задаваемые вопросы
NEWS = Новости и обновления

[database]
DATABASE_PATH = data/database.db

[crypto]
USDT_BEP20_ADDRESS = your_bep20_address
USDT_POLYGON_ADDRESS = your_polygon_address  
USDT_ERC20_ADDRESS = your_erc20_address

[referral]
LEVEL1_PERCENT = 10
LEVEL2_PERCENT = 5
LEVEL3_PERCENT = 2
```

## 🏗️ Архитектура

```
AutoCryptoShop/
├── tgbot/
│   ├── data/           # Конфигурация и загрузчики
│   ├── filters/        # Фильтры для обработчиков
│   ├── handlers/       # Обработчики команд и сообщений
│   ├── keyboards/      # Inline и reply клавиатуры
│   ├── middlewares/    # Промежуточное ПО
│   ├── services/       # Сервисы (БД, платежи)
│   └── utils/          # Утилиты и вспомогательные функции
├── data/               # База данных
├── main.py            # Точка входа
├── settings.ini       # Конфигурация
└── requirements.txt   # Зависимости
```

## 💾 База данных

Бот использует SQLite с автоматическим созданием следующих таблиц:

- **users** - пользователи и их данные
- **settings** - настройки бота
- **payment_systems** - платежные системы
- **categories** - категории товаров
- **subcategories** - подкатегории
- **items** - товары
- **goods** - конкретные позиции товаров
- **promocodes** - промокоды
- **purchases** - покупки
- **transactions** - транзакции

## 🔧 Функционал

### Для пользователей:
- 🛍️ Просмотр каталога товаров
- 💳 Покупка через криптовалюты
- 🎁 Использование промокодов
- 👥 Реферальная программа
- 📊 Личная статистика
- 🌐 Смена языка интерфейса

### Для администраторов:
- 📝 Управление товарами и категориями
- 💰 Настройка платежных систем
- 👤 Управление пользователями
- 🎫 Создание промокодов
- 📊 Статистика и аналитика
- 📢 Рассылка сообщений
- ⚙️ Общие настройки бота

## 🛡️ Безопасность

- ✅ Защита от спама через middleware
- ✅ Проверка подписки на канал
- ✅ Валидация входных данных
- ✅ Логирование всех операций
- ✅ Автоматические бэкапы БД

## 📈 Мониторинг

Бот включает систему логирования с цветовой индикацией:
- 🟢 **INFO** - обычные операции
- 🟡 **WARNING** - предупреждения
- 🔴 **ERROR** - ошибки
- 🟣 **DEBUG** - отладочная информация

## 🔄 Автоматизация

Встроенный планировщик задач (APScheduler):
- Ежедневное обновление статистики
- Еженедельные отчеты
- Автоматические бэкапы базы данных
- Очистка устаревших данных

## 🌍 Многоязычность

Поддерживаемые языки:
- 🇷🇺 Русский (по умолчанию)
- 🇺🇸 English

Добавление нового языка:
1. Создайте файл в `tgbot/data/locales/`
2. Переведите все ключи из базового языка
3. Обновите список языков в настройках

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции (`git checkout -b feature/AmazingFeature`)
3. Зафиксируйте изменения (`git commit -m 'Add some AmazingFeature'`)
4. Запушьте в ветку (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

## 📝 Лицензия

Этот проект распространяется под лицензией MIT. См. файл `LICENSE` для подробностей.

## 📞 Поддержка

- 📧 Email: support@example.com
- 💬 Telegram: @support_username
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/AutoCryptoShop/issues)

## 📊 Статус проекта

![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)
![aiogram Version](https://img.shields.io/badge/aiogram-3.20.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

---

⭐ Если проект был полезен, поставьте звездочку!

**Разработано с ❤️ для автоматизации торговли** 