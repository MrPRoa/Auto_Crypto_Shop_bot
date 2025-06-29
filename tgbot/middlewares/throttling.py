# - *- coding: utf- 8 - *-
import asyncio
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from tgbot.utils.utils_functions import get_admins
from tgbot.utils.translations import get_text, get_user_language
from typing import Callable, Dict, Any, Awaitable, Union


# Мидлварь для антиспама
class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit=0.5):
        self.rate_limit = limit
        self.storage = {}  # Простое хранилище для тротлинга
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[Union[Message, CallbackQuery], Dict[str, Any]], Awaitable[Any]],
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any]
    ) -> Any:
        
        user_id = event.from_user.id
        current_time = asyncio.get_event_loop().time()
        
        # Админы не тротлятся
        if user_id in get_admins():
            return await handler(event, data)
            
        # Проверяем последнее сообщение пользователя
        last_time = self.storage.get(user_id, 0)
        
        if current_time - last_time < self.rate_limit:
            # Тротлинг активен
            lang = get_user_language(user_id)
            if isinstance(event, Message):
                await event.reply(get_text(lang, 'no_spam'))
            elif isinstance(event, CallbackQuery):
                await event.answer(get_text(lang, 'no_spam_alert'), show_alert=True)
            return
            
        # Обновляем время последнего сообщения
        self.storage[user_id] = current_time
        
        return await handler(event, data)


# Изменение лимитов отправки сообщения у декораторов
def rate_limit(limit: int):
    def decorator(func):
        setattr(func, "throttling_rate_limit", limit)
        return func
    return decorator
