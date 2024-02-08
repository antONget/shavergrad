from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import logging

router = Router()


@router.callback_query()
async def all_calback(callback: CallbackQuery) -> None:
    logging.info(f'all_calback: {callback.message.chat.id}')
    print(callback.data)

@router.message()
async def all_message(message: Message) -> None:
    logging.info(f'all_message')
    if message.photo:
        print(message.photo[-1].file_id)