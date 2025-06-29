# - *- coding: utf- 8 - *-
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from tgbot.services.sqlite import get_settings

class IsSub(BaseFilter):
    """Фильтр проверки подписки"""
    async def __call__(self, obj: Message | CallbackQuery) -> bool:
        settings = get_settings()
        
        if settings and settings.get('is_sub') == "True":
            # Здесь должна быть логика проверки подписки
            # Пока что возвращаем False (пользователь подписан)
            return False
        
        # Если проверка подписки отключена, пропускаем фильтр
        return False