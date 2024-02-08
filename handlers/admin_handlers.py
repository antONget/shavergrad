from aiogram import Router, F
import logging
import requests

from aiogram.filters import CommandStart,StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from config_data.config import Config, load_config
from module.database import create_table_dish, create_table_promotion, insert_role_admin, create_table_admin
from keyboards.keyboards_admin import keyboards_superadmin, keyboard_edit_menu, keyboard_edit_promotion, \
    keyboard_role_admin

router = Router()
config: Config = load_config()
user_dict = {}

class Admin(StatesGroup):
    role = State()


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


@router.message(F.text == '⚙️ Администраторы 👥', lambda message: str(message.chat.id) == str(config.tg_bot.admin_ids))
async def press_button_setting_administrator(message: Message) -> None:
    logging.info(f'press_button_setting_administrator: {message.chat.id}')
    create_table_admin()
    await message.answer(text='Выберите роль для участника',
                         reply_markup=keyboard_role_admin())


@router.callback_query(F.data.startswith('role'))
async def select_role_admin(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Пришлите телеграм id пользователя. Убедитесь, что пользователь запускал бота')
    await state.set_state(Admin.role)
    await state.update_data(role=callback.data.split('_')[1])


@router.message(StateFilter(Admin.role))
async def set_role_user(message: Message, state: FSMContext):
    telegram_id = int(message.text)
    user_dict[message.chat.id] = await state.get_data()
    user = get_telegram_user(user_id=telegram_id, bot_token=config.tg_bot.token)
    if 'result' in user:
        insert_role_admin(telegram_id=telegram_id,
                          role=user_dict[message.chat.id]['role'])
        await message.answer(text=f'Пользователь добавлен в проект {user_dict[message.chat.id]["role"]}')
        await state.set_state(default_state)
    else:
        await message.answer(text='id не корректен, или пользователь не запустил бота')

def get_telegram_user(user_id, bot_token):
    url = f'https://api.telegram.org/bot{bot_token}/getChat'
    data = {'chat_id': user_id}
    response = requests.post(url, data=data)
    print()
    return response.json()