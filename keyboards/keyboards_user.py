from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import logging


def keyboard_confirm_phone():
    logging.info(f'keyboard_confirm_phone')
    button_1 = InlineKeyboardButton(text='Изменить телефон', callback_data='edit_phone')
    button_2 = InlineKeyboardButton(text='Продолжить', callback_data='continue_user')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1, button_2]])
    return keyboard


def keyboards_get_phone():
    button_1 = KeyboardButton(text='Поделиться', request_contact=True)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button_1]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard


def keyboards_main_menu():
    button_1 = KeyboardButton(text='Меню 🍴')
    button_2 = KeyboardButton(text='Акции')
    button_3 = KeyboardButton(text='Контакты 📞')
    button_4 = KeyboardButton(text='Корзина 🛒')
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button_1], [button_2], [button_3], [button_4]],
        resize_keyboard=True
    )
    return keyboard


def keyboards_list_category(list_category):
    print('keyboards_list_category')
    kb_builder = ReplyKeyboardBuilder()
    buttons = [
        KeyboardButton(text=f'{i}') for i in list_category
    ]
    button_home = [KeyboardButton(text='🏠')]
    kb_builder.row(*buttons, width=2)
    kb_builder.row(*button_home, width=1)
    return kb_builder.as_markup(resize_keyboard=True)


def keyboard_paydish(cost, id_dish):
    logging.info(f'keyboard_confirm_phone')
    button_1 = InlineKeyboardButton(text=f'Заказать за {cost}руб.', callback_data=f'paydish_{id_dish}')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1]])
    return keyboard


def keyboards_list_category_nav(list_category):
    print('keyboards_list_category_nav')
    kb_builder = ReplyKeyboardBuilder()
    buttons = [
        KeyboardButton(text=f'{i}') for i in list_category
    ]
    button_nav = [KeyboardButton(text='<< Назад'),
                  KeyboardButton(text='🏠'),
                  KeyboardButton(text='Вперед >>')]
    kb_builder.row(*buttons, width=2)
    kb_builder.row(*button_nav)
    return kb_builder.as_markup(resize_keyboard=True)


def keyboard_select_portion(portion):
    logging.info(f'keyboard_select_portion')
    button_1 = InlineKeyboardButton(text=f'+', callback_data=f'plus_portion')
    button_2 = InlineKeyboardButton(text=f'{portion}', callback_data=f'none')
    button_3 = InlineKeyboardButton(text=f'-', callback_data=f'minus_portion')
    button_4 = InlineKeyboardButton(text=f'Заказать', callback_data=f'order_dish')
    button_5 = InlineKeyboardButton(text=f'Отменить', callback_data=f'cancel_order_dish')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_3, button_2, button_1], [button_5, button_4]])
    return keyboard

def keyboard_continue_register():
    logging.info(f'keyboard_select_portion')
    button_1 = InlineKeyboardButton(text=f'Продолжить заказ', callback_data=f'continue_order')
    button_2 = InlineKeyboardButton(text=f'Оформить заказ', callback_data=f'register_order')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1, button_2]])
    return keyboard


def keyboard_confirm_register(id_order):
    logging.info(f'keyboard_confirm_register')
    button_1 = InlineKeyboardButton(text=f'Все верно!', callback_data=f'registerdone.{id_order}')
    button_2 = InlineKeyboardButton(text=f'Изменить заказ', callback_data=f'registerchange.{id_order}')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_2, button_1]])
    return keyboard


def keyboard_change_order(number_dish):
    logging.info(f'keyboard_change_order')
    button_1 = InlineKeyboardButton(text=f'<<<<', callback_data=f'back_dish')
    button_2 = InlineKeyboardButton(text=f'>>>>', callback_data=f'forward_dish')
    button_3 = InlineKeyboardButton(text=f'-', callback_data=f'minus_portion')
    button_4 = InlineKeyboardButton(text=f'{number_dish}', callback_data=f'none')
    button_5 = InlineKeyboardButton(text=f'+', callback_data=f'plus_portion')
    button_6 = InlineKeyboardButton(text=f'Продолжить', callback_data=f'done_change')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1, button_2],[button_3, button_4, button_5], [button_6]])
    return keyboard