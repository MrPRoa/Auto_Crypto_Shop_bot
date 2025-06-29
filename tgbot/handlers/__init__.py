# - *- coding: utf- 8 - *-
from aiogram import Dispatcher

def setup_handlers(dp: Dispatcher):
    """Регистрирует все обработчики"""
    
    # Импортируем и регистрируем все роутеры
    from . import main_start
    from . import admin_functions
    from . import users_refills
    from . import admin_payments
    from . import admin_products
    from . import user_products
    
    # Регистрируем роутеры
    dp.include_router(main_start.router)
    dp.include_router(admin_functions.router)
    dp.include_router(users_refills.router)
    dp.include_router(admin_payments.router)
    dp.include_router(admin_products.router)
    dp.include_router(user_products.router)

__all__ = ['setup_handlers']
