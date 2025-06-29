from aiogram.types import Message, CallbackQuery
from aiogram.filters import BaseFilter
from tgbot.utils.utils_functions import get_admins
from typing import Union

class IsAdmin(BaseFilter):
    async def __call__(self, update: Union[Message, CallbackQuery]) -> bool:
        if isinstance(update, Message):
            user_id = update.from_user.id
        else:  # CallbackQuery
            user_id = update.from_user.id
        return user_id in get_admins()