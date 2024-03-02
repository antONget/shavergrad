import logging
from typing import Any, Awaitable, Callable, Dict
from datetime import datetime, time
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


logger = logging.getLogger(__name__)

def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time



class FirstOuterMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        print('---')
        if not is_time_between(time(10-3, 30), time(23-3, 30)):
            text = 'Доставка доступна с 10:30 до 21:30, заходите в часы работы будем рады вас накормить'
            try:
                await event.answer(text=text)
            except:
                await event.message.answer(text=text)
            return
        result = await handler(event, data)
        return result