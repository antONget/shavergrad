from aiogram import Router, F
import logging

from aiogram.filters import CommandStart
from aiogram.types import Message

from config_data.config import Config, load_config
from module.database import create_table_dish, create_table_promotion
from keyboards.keyboards_admin import keyboards_superadmin, keyboard_edit_menu, keyboard_edit_promotion

router = Router()
config: Config = load_config()


@router.message(CommandStart(), lambda message: str(message.chat.id) == str(config.tg_bot.admin_ids))
async def process_start_command_admin(message: Message) -> None:
    logging.info(f'process_start_command_admin: {message.chat.id}')
    if str(message.chat.id) == str(config.tg_bot.admin_ids):
        keyboard = keyboards_superadmin()
        await message.answer('Выберите какой раздел вы хотите отредактировать',
                             reply_markup=keyboard)
    else:
        await message.answer('Вы юзер')


@router.message(F.text == '⚙️ Меню 🍽', lambda message: str(message.chat.id) == str(config.tg_bot.admin_ids))
async def press_button_setting_menu(message: Message) -> None:
    logging.info(f'press_button_setting_menu: {message.chat.id}')
    create_table_dish()
    keyboard = keyboard_edit_menu()
    await message.answer(text='Выберите пункт',
                         reply_markup=keyboard)


@router.message(F.text == '⚙️ Акции и скидки 🎁', lambda message: str(message.chat.id) == str(config.tg_bot.admin_ids))
async def press_button_setting_promotion(message: Message) -> None:
    logging.info(f'press_button_setting_promotion: {message.chat.id}')
    create_table_promotion()
    keyboard = keyboard_edit_promotion()
    await message.answer(text='Редактирование раздела "Скидки и акции"',
                         reply_markup=keyboard)


