# - *- coding: utf- 8 - *-
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from tgbot.services.sqlite import *
from tgbot.utils.utils_functions import send_admins
from tgbot.data.loader import bot
from typing import Callable, Dict, Any, Awaitable, Union

class ExistsUserMiddleware(BaseMiddleware):

    def __init__(self):
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[Union[Message, CallbackQuery], Dict[str, Any]], Awaitable[Any]],
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any]
    ) -> Any:
        
        user = event.from_user

        if user is not None and not user.is_bot:
            self.id = user.id
            self.user_name = user.username if user.username else ""
            self.first_name = user.first_name
            self.bot = await bot.get_me()

            # Не регистрируем пользователей автоматически - пусть это делает система выбора языка
            if get_user(id=self.id) is not None:
                if get_user(id=self.id)['is_ban'] == "" or get_user(id=self.id)['is_ban'] is None:
                    update_user(id=self.id, is_ban="False")
                if get_user(id=self.id)['user_name'] != self.user_name:
                    update_user(self.id, user_name=self.user_name)
                if get_user(id=self.id)['first_name'] != self.first_name:
                    update_user(self.id, first_name=self.first_name)
        
                if len(self.user_name) >= 1:
                    if self.user_name != get_user(id=self.id)['user_name']:
                        update_user(id=self.id, user_name=self.user_name)
                else:
                    update_user(id=self.id, user_name="")

        return await handler(event, data)