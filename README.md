# 🛒 AutoCryptoShop - Telegram Bot

Modern Telegram bot for automated trading with cryptocurrency payments support and multi-level referral system.

## ✨ Features

- 🤖 **Modern Architecture** - built on aiogram 3.20.0
- 💰 **Crypto Payments** - USDT support (BEP-20, Polygon, ERC-20)
- 🌍 **Multi-language** - Russian and English languages
- 👥 **Referral System** - 3 levels with customizable percentages
- 🎫 **Promo Code System** - flexible discounts and bonuses
- 📊 **Admin Panel** - complete bot management
- 🔄 **Automation** - task scheduler and auto-backups
- 📱 **Adaptive Interface** - beautiful inline keyboards

## 🚀 Quick Start

### Requirements

- Python 3.12+
- SQLite3
- Telegram Bot Token

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/AutoCryptoShop.git
cd AutoCryptoShop
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure settings:**
Edit the `settings.ini` file:
```ini
[settings]
BOT_TOKEN = your_bot_token_here
ADMINS = your_admin_id_here
SUPPORT_USER = @your_support_username
CHAT_ID = your_chat_id
```

4. **Run the bot:**
```bash
python main.py
# or for Windows
start.bat
```

## 📋 Configuration

### settings.ini
```ini
[settings]
BOT_TOKEN = 1234567890:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
ADMINS = 123456789,987654321
SUPPORT_USER = @support_username
CHAT_ID = -1001234567890
CHANNEL_URL = https://t.me/yourchannel
FAQ = Frequently Asked Questions
NEWS = News and Updates

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

## 🏗️ Architecture

```
AutoCryptoShop/
├── tgbot/
│   ├── data/           # Configuration and loaders
│   ├── filters/        # Handler filters
│   ├── handlers/       # Command and message handlers
│   ├── keyboards/      # Inline and reply keyboards
│   ├── middlewares/    # Middleware
│   ├── services/       # Services (DB, payments)
│   └── utils/          # Utilities and helper functions
├── data/               # Database
├── main.py            # Entry point
├── settings.ini       # Configuration
└── requirements.txt   # Dependencies
```

## 💾 Database

The bot uses SQLite with automatic creation of the following tables:

- **users** - users and their data
- **settings** - bot settings
- **payment_systems** - payment systems
- **categories** - product categories
- **subcategories** - subcategories
- **items** - products
- **goods** - specific product items
- **promocodes** - promo codes
- **purchases** - purchases
- **transactions** - transactions

## 🔧 Functionality

### For Users:
- 🛍️ Browse product catalog
- 💳 Purchase via cryptocurrencies
- 🎁 Use promo codes
- 👥 Referral program
- 📊 Personal statistics
- 🌐 Language switching

### For Administrators:
- 📝 Manage products and categories
- 💰 Configure payment systems
- 👤 User management
- 🎫 Create promo codes
- 📊 Statistics and analytics
- 📢 Message broadcasting
- ⚙️ General bot settings

## 🛡️ Security

- ✅ Spam protection via middleware
- ✅ Channel subscription verification
- ✅ Input data validation
- ✅ All operations logging
- ✅ Automatic DB backups

## 📈 Monitoring

The bot includes a logging system with color indication:
- 🟢 **INFO** - normal operations
- 🟡 **WARNING** - warnings
- 🔴 **ERROR** - errors
- 🟣 **DEBUG** - debug information

## 🔄 Automation

Built-in task scheduler (APScheduler):
- Daily statistics updates
- Weekly reports
- Automatic database backups
- Cleanup of outdated data

## 🌍 Multi-language Support

Supported languages:
- 🇷🇺 Russian (default)
- 🇺🇸 English

Adding a new language:
1. Create a file in `tgbot/data/locales/`
2. Translate all keys from the base language
3. Update the language list in settings

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## 📞 Support

- 📧 Email: support@example.com
- 💬 Telegram: @support_username
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/AutoCryptoShop/issues)

## 📊 Project Status

![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)
![aiogram Version](https://img.shields.io/badge/aiogram-3.20.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

---

⭐ If this project was helpful, please give it a star!

**Developed with ❤️ for trading automation** 