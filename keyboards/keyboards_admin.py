from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import logging


def keyboards_superadmin():

    button_1 = KeyboardButton(text='⚙️ Администраторы 👥')
    button_2 = KeyboardButton(text='⚙️ Меню 🍽')
    button_3 = KeyboardButton(text='⚙️ Акции и скидки 🎁')
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button_1], [button_2, button_3]],
        resize_keyboard=True
    )
    return keyboard
def keyboards_manager():

    button_1 = KeyboardButton(text='⚙️ Администраторы 👥')
    button_2 = KeyboardButton(text='⚙️ Меню 🍽')
    button_3 = KeyboardButton(text='⚙️ Акции и скидки 🎁')
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button_1], [button_2, button_3]],
        resize_keyboard=True
    )
    return keyboard

# МЕНЮ settngs
def keyboard_edit_menu():
    """
    Клавиатура для редактирования списка администраторов
    :return:
    """
    button_1 = InlineKeyboardButton(text='Добавить', callback_data='add_dish')
    button_2 = InlineKeyboardButton(text='Удалить', callback_data='delete_dish')
    button_3 = InlineKeyboardButton(text='Редактировать', callback_data='edit_dish')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1, button_2, button_3]])
    return keyboard


# АКЦИИ И СКИДКИ settngs
def keyboard_edit_promotion():
    """
    Клавиатура для редактирования списка администраторов
    :return:
    """
    button_1 = InlineKeyboardButton(text='Добавить', callback_data='add_promotion')
    button_2 = InlineKeyboardButton(text='Удалить', callback_data='delete_promotion')
    button_3 = InlineKeyboardButton(text='Удалить все акции', callback_data='delete_all_promotion')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1, button_2], [button_3]])
    return keyboard


# БЛЮДО - Добавить
def keyboard_dish_in_stop():
    button_1 = InlineKeyboardButton(text='Да, его можно заказать!', callback_data='dish_not_in_stop')
    button_2 = InlineKeyboardButton(text='Блюдо, пока не доступно.', callback_data='dish_in_stop')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2]])
    return keyboard


# БЛЮДО - Добавить
def keyboard_confirmation_add_dish():
    button_1 = InlineKeyboardButton(text='Добавить!', callback_data='add_dish_done')
    button_2 = InlineKeyboardButton(text='Отмена', callback_data='cancel_add_dish')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2]])
    return keyboard


# БЛЮДО - Добавить
def keyboard_continue_add_dish():
    button_1 = InlineKeyboardButton(text='Добавить еще блюда', callback_data='continue_add_dish')
    button_2 = InlineKeyboardButton(text='Завершить', callback_data='finish_add_dish')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2]])
    return keyboard


# МЕНЮ - РЕДАКТИРОВАТЬ
def keyboards_select_dish_edit_menu(list_data_button, list_id_callback, back, forward, count, str_callback_button):
    logging.info(f'keyboards_select_dish_edit_menu')
    # проверка чтобы не ушли в минус
    if back < 0:
        back = 0
        forward = 2
    # считаем сколько всего блоков по заданному количество элементов в блоке
    count_users = len(list_data_button)
    whole = count_users // count
    remains = count_users % count
    max_forward = whole + 1
    # если есть остаток, то увеличиваем количество блоков на один, чтобы показать остаток
    if remains:
        max_forward = whole + 2
    # проверка, что бы не уйти в блоки без значений
    if forward > max_forward:
        forward = max_forward
        back = forward - 2
    kb_builder = InlineKeyboardBuilder()
    buttons = []
    print(list_data_button, count_users, back, forward, max_forward)
    list_id_block = list_id_callback[back*count:(forward-1)*count]
    list_name_button_block = list_data_button[back*count:(forward-1)*count]
    # выбираем срез значений из списка по номеру блока
    for name_button, id_button in zip(list_name_button_block, list_id_block):
        # print(name_button, id_button)
        button = f'{str_callback_button}textbutton_{id_button}'
        buttons.append(InlineKeyboardButton(
            text=name_button,
            callback_data=button))
    button_back = InlineKeyboardButton(text='<<<<',
                                       callback_data=f'{str_callback_button}back_{str(back)}')
    button_count = InlineKeyboardButton(text=f'{back+1}',
                                        callback_data='none')
    button_next = InlineKeyboardButton(text='>>>>',
                                       callback_data=f'{str_callback_button}forward_{str(forward)}')

    kb_builder.row(*buttons, width=1)
    kb_builder.row(button_back, button_count, button_next)

    return kb_builder.as_markup()


# БЛЮДО - Редактировать - Выбор атрибута для редакции блюда
def keyboard_edit_attribute_dish(is_stop):
    if is_stop:
        stop = '❌'
    else:
        stop = '✅'
    button_1 = InlineKeyboardButton(text='Категория', callback_data='edit_attribute_category')
    button_2 = InlineKeyboardButton(text='Наименование', callback_data='edit_attribute_name')
    button_3 = InlineKeyboardButton(text='Фотография', callback_data='edit_attribute_id_photo')
    button_4 = InlineKeyboardButton(text='Описание', callback_data='edit_attribute_description')
    button_5 = InlineKeyboardButton(text='Стоимость', callback_data='edit_attribute_cost')
    button_6 = InlineKeyboardButton(text=f'Можно заказать {stop}', callback_data='edit_attribute_is_stop')
    button_7 = InlineKeyboardButton(text='Все правильно', callback_data='edit_attribute_done')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2], [button_3], [button_4], [button_5], [button_6], [button_7]])
    return keyboard

def keyboard_back():
    button_1 = InlineKeyboardButton(text='Hазад', callback_data='back_edit_attribute')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1]])
    return keyboard


# УДАЛИТЬ -
def keyboard_delete_select_dish():
    button_1 = InlineKeyboardButton(text='Удалить', callback_data='delete_select_dish')
    button_2 = InlineKeyboardButton(text='Отмена', callback_data='cancel_delete_select_dish')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2]])
    return keyboard


# АКЦИИ
def keyboard_pass_add_photo_promotion():
    button_1 = InlineKeyboardButton(text='Пропустить', callback_data='pass_add_photo_promotion')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1]])
    return keyboard


def keyboard_confirm_add_promotion():
    button_1 = InlineKeyboardButton(text='Добавить', callback_data='confirm_add_promotion')
    button_2 = InlineKeyboardButton(text='Отмена', callback_data='cancel_add_promotion')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2]])
    return keyboard

def keyboard_confirm_del_promotion():
    button_1 = InlineKeyboardButton(text='Удалить', callback_data='confirm_del_promotion')
    button_2 = InlineKeyboardButton(text='Отмена', callback_data='cancel_del_promotion')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2]])
    return keyboard


def keyboard_confirm_del_all_promotion():
    button_1 = InlineKeyboardButton(text='Удалить все акции', callback_data='confirm_del_all_promotion')
    button_2 = InlineKeyboardButton(text='Отмена', callback_data='cancel_del_all_promotion')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2]])
    return keyboard


def keyboard_role_admin():
    button_1 = InlineKeyboardButton(text='Менеджер', callback_data='role_manager')
    button_2 = InlineKeyboardButton(text='Курьер', callback_data='role_courier')
    button_3 = InlineKeyboardButton(text='Повар', callback_data='role_cook')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2], [button_3]])
    return keyboard