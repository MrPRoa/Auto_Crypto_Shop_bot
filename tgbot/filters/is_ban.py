from aiogram.types import Message, CallbackQuery
from aiogram.filters import BaseFilter
from tgbot.services.sqlite import get_user
from tgbot.utils.utils_functions import get_admins
from typing import Union

class IsBan(BaseFilter):
    async def __call__(self, update: Union[Message, CallbackQuery]) -> bool:
        if isinstance(update, Message):
            user_id = update.from_user.id
        else:  # CallbackQuery
            user_id = update.from_user.id
            
        user = get_user(id=user_id)
        if user and user['is_ban'] == "True" and user_id not in get_admins():
            return True
        else:
            return False
            
