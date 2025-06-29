from aiogram.types import Message, CallbackQuery
from aiogram.filters import BaseFilter
from tgbot.services.sqlite import get_settings
from typing import Union

class IsRefill(BaseFilter):
    async def __call__(self, update: Union[Message, CallbackQuery]) -> bool:
        if get_settings()['is_refill'] == "True":
            return False
        else:
            return True