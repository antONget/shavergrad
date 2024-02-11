from module.database import select_all_manager, select_all_category_table_dish
from aiogram.types import Message
from config_data.config import load_config, Config
import logging

config : Config = load_config()
def chek_manager(telegram_id):
    logging.info('chek_manager')
    list_manager = select_all_manager('manager')
    print(list_manager, config.tg_bot.admin_ids, ':',telegram_id)

    print(telegram_id in list_manager or telegram_id == config.tg_bot.admin_ids)
    return (telegram_id in list_manager or telegram_id == config.tg_bot.admin_ids)


def filter_category(category):
    list_category = select_all_category_table_dish()
    logging.info(f'filter_category: {category} {category in list_category}')
    return category in list_category

def comand_user_admin(message: Message):
    logging.info('comand_user_admin')
    if chek_manager(message.chat.id) or str(message.chat.id) == str(config.tg_bot.admin_ids):
        print(message.text)
        return message.text == '/user'