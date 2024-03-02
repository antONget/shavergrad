from aiogram import Router, F, Bot
import logging
import asyncio
import datetime
import requests
from services.geolocation import check_adress, check_adress_lon_alt
import re
from aiogram.filters import CommandStart, and_f, or_f, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext
from config_data.config import Config, load_config
from module.database import create_table_user, select_row_table_users, insert_data_table_users,\
    select_all_category_table_dish, select_all_data_table_promotion, select_dish_in_category, select_row_id_dish, \
    insert_data_table_number_order, create_table_number_order, create_table_orders, insert_data_table_orders, \
    select_row_table_number_order, update_table_orders, select_data_table_orders_to_order_id, \
    select_data_table_orders_idorder_iddish, update_status_table_number_id_order, update_status_table_number_adress, \
    update_status_table_number_comment, select_all_manager, select_data_table_orders, select_id_number_order, \
    update_phone_users, delete_table_orders
from keyboards.keyboards_user import keyboard_confirm_phone, keyboards_get_phone, keyboards_main_menu,\
    keyboards_list_category, keyboard_paydish, keyboards_list_category_nav, keyboard_select_portion, \
    keyboard_continue_register, keyboard_confirm_register, keyboard_change_order, keyboard_pass_comment, keyboard_get_location
from filter.admin_filter import filter_category, comand_user_admin
from services.call_phone import call_to_phone
#
router = Router()
config: Config = load_config()
#
#
class Form_user(StatesGroup):
    name_user = State()
    phone_user = State()
    adress_user = State()
    comment_order = State()
#
user_dict = {}


def get_telegram_user(user_id: int, bot_token: str) -> dict:
    """
    Проверка пользователя на взаимодействие с ботом
    :param user_id: telegram_id пользователя
    :param bot_token: TOKEN бота
    :return: словарь с ответом
    """
    url = f'https://api.telegram.org/bot{bot_token}/getChat'
    data = {'chat_id': user_id}
    response = requests.post(url, data=data)
    print(response.json())
    return response.json()


def validate_russian_phone_number(phone_number):
    # Паттерн для российских номеров телефона
    # Российские номера могут начинаться с +7, 8, или без кода страны
    pattern = re.compile(r'^(\+7|8|7)?(\d{10})$')

    # Проверка соответствия паттерну
    match = pattern.match(phone_number)

    return bool(match)

@router.message(or_f(CommandStart(), lambda message: comand_user_admin(message)))
async def process_start_command_user(message: Message, state: FSMContext) -> None:
    logging.info(f'process_start_command_admin: {message.chat.id}')
    create_table_user()
    await message.answer(text=f"Друзья, вас приветствуют «Шаверград»!\n"
                              f"Всегда рады накормить вкуснейшей шавермой и мощнейшими бургерами.")
    await asyncio.sleep(3)
    await message.answer(text="Вы можете:\n"
                              "🍽️ прийти к нам в кафе по адресу: Вишерская улица, 2 (график работы: 10:00-23:00)\n"
                              "🤳или заказать доставку в этом боте с 10:30 до 22:30.")
    row_user = select_row_table_users(message.chat.id)
    # print(row_user)
    if not row_user:
        await message.answer(text='Как вас зовут?')
        await state.set_state(Form_user.name_user)
    else:
        await message.answer(text=f'{row_user[2]}, рады видеть вас снова!\n'
                                  f'телефон: {row_user[3]}',
                             reply_markup=keyboard_confirm_phone())


@router.message(F.text, StateFilter(Form_user.name_user))
async def get_name_user(message: Message, state: FSMContext) -> None:
    await state.update_data(user_name=message.text)
    await message.answer(text='Укажите ваш номер телефона или нажмите внизу «Поделиться» 👇',
                         reply_markup=keyboards_get_phone())
    await state.set_state(Form_user.phone_user)


@router.callback_query(F.data == 'edit_phone')
async def press_button_edit_phone(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'press_button_edit_phone: {callback.message.chat.id}')
    # await state.update_data(user_name=callback.message.text)
    await callback.message.answer(text='Укажи свой телефон',
                                  reply_markup=keyboards_get_phone())
    await state.set_state(Form_user.phone_user)


@router.callback_query(F.data == 'continue_user')
async def press_button_continue_user(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'press_button_continue_user: {callback.message.chat.id}')
    await callback.message.answer(text='Для онлайн-заказа перейдите в раздел «🍴Меню». Если вы не завершили предыдущий '
                                       'заказ, обратите внимание на корзину.',
                                  reply_markup=keyboards_main_menu())
    await state.set_state(default_state)


@router.message(StateFilter(Form_user.phone_user))
async def get_phone_user(message: Message, state: FSMContext) -> None:
    logging.info(f'get_phone_user: {message.chat.id}')
    if message.contact:
        phone = str(message.contact.phone_number)
        # print(phone)
    else:
        phone = message.text
        if not validate_russian_phone_number(phone):
            await message.answer(text="Неверный формат номера, повторите ввод.")
            return
    await state.update_data(user_phone=phone)
    user_dict[message.chat.id] = await state.get_data()
    if not select_row_table_users(message.chat.id):
        insert_data_table_users(telegram_id=message.chat.id,
                                name=user_dict[message.chat.id]['user_name'],
                                phone=user_dict[message.chat.id]['user_phone'])
    else:
        update_phone_users(telegram_id=message.chat.id,
                           phone=phone)
    await message.answer(text="Для того, чтобы ознакомиться с меню или сделать онлайн-заказ на доставку, используйте"
                              " выпадающую клавиатуру на панели чата с ботом: «🍴Меню ».")
    await message.answer(text='При необходимости вы можете выбрать другие разделы или вернуться 🏠 в главное меню.',
                         reply_markup=keyboards_main_menu())
    await state.set_state(default_state)
#
#
@router.message(F.text == '🏠')
async def press_button_home(message: Message):
    await message.answer(text='Выберите раздел',
                         reply_markup=keyboards_main_menu())


@router.message(F.text == '📞 Контакты')
async def press_button_contact(message: Message):
    await message.answer_photo(photo='AgACAgIAAxkBAAIBq2XIoTRjF0VDFI7Dywq5fazj3hrBAAKk2zEbczhISps0ZgABYONr5gEAAwIAA3gAAzQE',
                               caption="""К сожалению в Яндекс картах нас пока нет, но мы это исправляем! Ориентир: внешняя часть угла дома

10:00-23:00 без перерывов и выходных
Вишерская улица 2""")
#
#
@router.message(F.text == '🏷️ Акции')
async def press_button_promotion(message: Message):
    list_promotion = select_all_data_table_promotion()
    for promo in list_promotion:
        # print(promo)
        if promo[2] != 'none':
            await message.answer_photo(photo=promo[2],
                                       caption=promo[1])
        else:
            await message.answer(text=promo[1])
#
#
@router.message(F.text == '🍴 Меню')
async def press_button_menu(message: Message):
    list_category = select_all_category_table_dish()
    keyboard = keyboards_list_category(list_category)
    await message.answer(text=f"Минимальная сумма заказа: <b>600 руб.</b>\n"
                              f"Выберите блюдо:",
                         reply_markup=keyboard)
#
#
@router.message(lambda message: filter_category(message.text))
async def press_button_category(message: Message, state: FSMContext):
    logging.info(f'press_button_category: {message.chat.id}')
    category = message.text
    print(category)
    await state.update_data(select_category=category)
    await state.update_data(num_block=1)
    # получаем список айди и названий блюд в категории не в стоп списке
    list_id_dish_category = select_dish_in_category(category)
    # получаем информацию о блюде первой в списке по его айди
    info_dish = select_row_id_dish(list_id_dish_category[0][0])
    await message.answer_photo(photo=info_dish[5],
                               caption=f'<b>{info_dish[1]}</b>\n\n'
                                       f'Описание: {info_dish[4]}\n',
                               reply_markup=keyboard_paydish(cost=info_dish[2], id_dish=info_dish[0],
                                                             list_id_dish_category=list_id_dish_category))




# @router.message(lambda message: filter_category(message.text))
# async def press_button_category(message: Message, state: FSMContext):
#     # logging.info(f'press_button_category: {message.chat.id}')
#     category = message.text
#     print(category)
#     await state.update_data(select_category=category)
#     await state.update_data(num_block=1)
#     list_id_dish_category = select_dish_in_category(category)
#     # print(list_id_dish_category)
#     back = 0
#     forward = 2
#     count = 3
#
#     len_list = len(list_id_dish_category)
#     int_block = len_list // count
#     remain_block = len_list % count
#     if remain_block:
#         int_block += 1
#     for id_dish in list_id_dish_category[back*count:(forward-1)*count]:
#         # print('id_dish', id_dish)
#         row_dish = select_row_id_dish(id_dish[0])
#         # print('row_dish', row_dish)
#         # если не в стоп листе
#         if not row_dish[-1]:
#             await message.answer_photo(photo=row_dish[-2],
#                                        caption=f'Название: {row_dish[1]}\n'
#                                                f'Состав: {row_dish[4]}',
#                                        reply_markup=keyboard_paydish(row_dish[2], row_dish[0]))
#     list_category = select_all_category_table_dish()
#     await message.answer(text=f"Для выбора других позиций в категории <b>{category}</b> листайте\n"
#                               f" ⏪ Назад 🏠 Вперед ⏩ "
#                               f"на клавиатуре 👇",
#                          reply_markup=keyboards_list_category_nav(list_category))
# #
# #
# @router.message(or_f(F.text == '<< Назад', F.text == 'Вперед >>'))
# async def press_button_back_forward(message: Message, state: FSMContext):
#     """
#     Функция реагирует на нажатие на кнопки навигации - << Назад и Вперед >> увеличивая
#     номер выводимо блока с карточками блюд
#     :param message:
#     :param state:
#     :return:
#     """
#     logging.info(f'press_button_back_forward: {message.chat.id}')
#     user_dict[message.chat.id] = await state.get_data()
#     category = user_dict[message.chat.id]['select_category']
#     num_block = user_dict[message.chat.id]['num_block']
#     print("num_block", num_block)
#     list_id_dish_category = select_dish_in_category(category)
#     print(list_id_dish_category)
#     count = 3
#     len_list = len(list_id_dish_category)
#     int_block = len_list // count
#     remain_block = len_list % count
#     if remain_block:
#         int_block += 1
#     print('int_block: ', int_block)
#     back = 0
#     forward = 1
#     if message.text == '<< Назад':
#         num_block -= 1
#         if num_block == 1:
#             back = 0
#             forward = 2
#             await state.update_data(num_block=back+1)
#         else:
#             back = num_block - 1
#             forward = num_block + 1
#             await state.update_data(num_block=back+1)
#     elif message.text == 'Вперед >>':
#         num_block += 1
#         if num_block == int_block:
#             back = int_block - 1
#             forward = int_block + 1
#             await state.update_data(num_block=back+1)
#         else:
#             back = num_block - 1
#             forward = num_block + 1
#             await state.update_data(num_block=back+1)
#
#     print('back:', back, 'forward:', forward)
#     for id_dish in list_id_dish_category[back*count:(forward-1)*count]:
#         # print('id_dish', id_dish)
#         row_dish = select_row_id_dish(id_dish[0])
#         # print('row_dish', row_dish)
#         # если не в стоп листе
#         if not row_dish[-1]:
#             await message.answer_photo(photo=row_dish[-2],
#                                        caption=f'Название: {row_dish[1]}\n'
#                                                f'Состав: {row_dish[4]}',
#                                        reply_markup=keyboard_paydish(row_dish[2], row_dish[0]))
#     list_category = select_all_category_table_dish()
#     await message.answer(text=f"Для выбора других позиций в категории <b>{category}</b> листайте\n"
#                               f" ⏪ Назад 🏠 Вперед ⏩ "
#                               f"на клавиатуре 👇",
#                          reply_markup=keyboards_list_category_nav(list_category))
#
#
@router.callback_query(F.data.startswith('showdish'))
async def press_button_show_dish(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Функция реагирует на нажатие на блюдо для показа его карточки
    :param callback: передается showdish_id_dish
    :param state:
    :return:
    """
    logging.info(f'press_button_payment_dish: {callback.message.chat.id}')
    id_dish = int(callback.data.split('_')[1])
    info_dish = select_row_id_dish(id_dish)
    user_dict[callback.message.chat.id] = await state.get_data()
    category = user_dict[callback.message.chat.id]['select_category']
    list_id_dish_category = select_dish_in_category(category)
    print(callback.message.message_id)
    await bot.delete_message(chat_id=callback.message.chat.id,
                             message_id=(callback.message.message_id))
    await callback.message.answer_photo(photo=info_dish[5],
                                        caption=f'<b>{info_dish[1]}</b>\n\n'
                                                f'Описание: {info_dish[4]}\n',
                                        reply_markup=keyboard_paydish(cost=info_dish[2], id_dish=info_dish[0],
                                                                      list_id_dish_category=list_id_dish_category))


@router.callback_query(F.data.startswith('paydish'))
async def press_button_payment_dish(callback: CallbackQuery, state: FSMContext):
    """
    Функция реагирует на нажатие на кнопку "Заказать" на карточки товара
    :param callback: передается paydish_id_dish
    :param state:
    :return:
    """
    logging.info(f'press_button_payment_dish: {callback.message.chat.id}')
    id_dish = int(callback.data.split('_')[1])
    info_dish = select_row_id_dish(id_dish)
    # формирование строки даты для номера заказа
    current_date = datetime.datetime.now()
    current_date_string = current_date.strftime('%m/%d/%y_%H:%M:%S')
    # уникальный номер заказа
    number_order = f'{callback.message.chat.id}_{current_date_string}'
    create_table_number_order()
    # получаем список заказов пользователя
    data_number_order = select_row_table_number_order(telegram_id=callback.message.chat.id)
    print('data_number_order', data_number_order)
    # если пользователь уже делал заказы, то список не пустой
    if data_number_order:
        # его последний заказ завершен, то создаем новый номер заказа и устанавливаем статус 0
        if data_number_order[-1][-1]:
            insert_data_table_number_order(id_order=number_order, telegram_id=callback.message.chat.id, status_order=0)
        # иначе продолжаем добавлять блюда к этому номеру заказа
        else:
            number_order = data_number_order[-1][1]
    # пользователь еще не делал заказов, добавляем новый номер заказа
    else:
        insert_data_table_number_order(id_order=number_order, telegram_id=callback.message.chat.id, status_order=0)
    create_table_orders()
    insert_data_table_orders(telegram_id=callback.message.chat.id, order_id=number_order, dish_id=id_dish, portion=1)
    list_category = select_all_category_table_dish()
    await state.update_data(portion=1)
    await state.update_data(id_dish=id_dish)
    await state.update_data(id_order=number_order)
    portion_old = select_data_table_orders_idorder_iddish(callback.message.chat.id, number_order, id_dish)
    await callback.message.answer(text=f'Вы выбрали '
                                       f'{info_dish[1]}',
                                  reply_markup=keyboards_list_category(list_category))
    await callback.message.answer(text=f'Укажите количество порций.',
                                  reply_markup=keyboard_select_portion(portion=portion_old[0][0]))
#
#
@router.callback_query(F.data.endswith('portion'))
async def press_button_payment_dish(callback: CallbackQuery, state: FSMContext):
    logging.info(f'press_button_payment_dish: {callback.message.chat.id}')
    user_dict[callback.message.chat.id] = await state.get_data()
    portion = user_dict[callback.message.chat.id]['portion']
    if callback.data.split('_')[0] == 'plus':
        portion += 1
        await state.update_data(portion=portion)
    elif callback.data.split('_')[0] == 'minus':
        portion -= 1
        if portion >= 0:
            await state.update_data(portion=portion)
        else:
            portion = 0
    try:
        await callback.message.edit_text(text=f'Укажите количество порций.',
                                         reply_markup=keyboard_select_portion(portion=portion))
    except:
        await callback.message.edit_text(text=f'Укажитe количество порций.',
                                         reply_markup=keyboard_select_portion(portion=portion))
#
#
@router.callback_query(F.data == 'order_dish')
async def press_button_order_dish(callback: CallbackQuery, state: FSMContext):
    logging.info(f'press_button_order_dish: {callback.message.chat.id}')
    user_dict[callback.message.chat.id] = await state.get_data()
    if user_dict[callback.message.chat.id]['portion']:
        update_table_orders(telegram_id=callback.message.chat.id,
                            dish_id=user_dict[callback.message.chat.id]['id_dish'],
                            order_id=user_dict[callback.message.chat.id]['id_order'],
                            portion=user_dict[callback.message.chat.id]['portion'])
        await callback.message.answer(text='Блюдо добавлено в корзину. Желаете что-то ещё добавить в свой заказ?',
                                      reply_markup=keyboard_continue_register())
    else:
        list_category = select_all_category_table_dish()
        keyboard = keyboards_list_category(list_category)
        await callback.message.answer(text=f"Блюдо отменено. Продолжите выбор блюд 👇",
                                      reply_markup=keyboard)
#
#
@router.callback_query(F.data == 'cancel_order_dish')
async def press_button_cancel_order_dish(callback: CallbackQuery, state: FSMContext):
    logging.info(f'press_button_cancel_order_dish: {callback.message.chat.id}')
    list_category = select_all_category_table_dish()
    keyboard = keyboards_list_category(list_category)
    await callback.message.answer(text=f"Блюдо отменено. Продолжите выбор блюд 👇",
                                  reply_markup=keyboard)


@router.callback_query(F.data == 'continue_order')
async def press_button_continue_order(callback: CallbackQuery, state: FSMContext):
    logging.info(f'press_button_continue_order: {callback.message.chat.id}')
    list_category = select_all_category_table_dish()
    keyboard = keyboards_list_category(list_category)
    await callback.message.answer(text=f"Продолжите выбор блюд 👇",
                                  reply_markup=keyboard)
#
#
@router.callback_query(F.data == 'register_order')
async def press_button_register_order(callback: CallbackQuery):
    logging.info(f'press_button_register_order: {callback.message.chat.id}')
    last_number_orders = select_row_table_number_order(callback.message.chat.id)[-1]
    print(last_number_orders)
    if last_number_orders[-1] == 0:
        order_id = last_number_orders[1]
        print('order_id', order_id)
        info_dish_last_order = select_data_table_orders_to_order_id(order_id=order_id)
        name = ''
        total = 0
        for i, info_order in enumerate(info_dish_last_order):
            info_dish = select_row_id_dish(info_order[3])
            name = name+f'{i+1}. {info_dish[1]}: {info_dish[2]} x {info_order[4]} = {info_dish[2] * info_order[4]} руб.\n'
            total += info_dish[2]*info_order[4]
        idorder = select_id_number_order(order_id)
        if total > 600:
            await callback.message.answer(text=f'Номер заказа: {idorder[0]}\n'
                                               f'{name}\n\n'
                                               f'Сумма заказа: {total} руб.',
                                          reply_markup=keyboard_confirm_register(order_id))
        else:
            await callback.message.answer(text=f'Номер заказа: {idorder[0]}\n'
                                               f'{name}\n\n'
                                               f'Сумма заказа: {total} руб.'
                                               f'\n\n'
                                               f'Минимальная сумма заказа 600 руб.')
#

async def press_button_register_order1(callback: CallbackQuery):
    logging.info(f'press_button_register_order1: {callback.message.chat.id}')
    last_number_orders = select_row_table_number_order(callback.message.chat.id)[-1]
    print(last_number_orders)
    if last_number_orders[-1] == 0:
        order_id = last_number_orders[1]
        print('order_id', order_id)
        info_dish_last_order = select_data_table_orders_to_order_id(order_id=order_id)
        name = ''
        total = 0
        for i, info_order in enumerate(info_dish_last_order):
            info_dish = select_row_id_dish(info_order[3])
            name = name+f'{i+1}. {info_dish[1]}: {info_dish[2]} x {info_order[4]} = {info_dish[2] * info_order[4]} руб.\n'
            total += info_dish[2]*info_order[4]
        idorder = select_id_number_order(order_id)
        if total > 600:
            await callback.message.answer(text=f'Номер заказа: {idorder[0]}\n'
                                               f'{name}\n\n'
                                               f'Сумма заказа: {total} руб.',
                                          reply_markup=keyboard_confirm_register(order_id))
        else:
            await callback.message.answer(text=f'Номер заказа: {idorder[0]}\n'
                                               f'{name}\n\n'
                                               f'Сумма заказа: {total} руб.'
                                               f'\n\n'
                                               f'Минимальная сумма заказа 600 руб.')

#
@router.callback_query(F.data.startswith('registerdone'))
async def press_button_register_all_done(callback: CallbackQuery, state: FSMContext):
    logging.info(f'press_button_register_all_done: {callback.message.chat.id}')
    print('press_button_register_all_done')
    id_order = callback.data.split('.')[1]
    # if id_order
    print('id_order-done', id_order)
    await state.update_data(register_order=id_order)
    update_status_table_number_id_order(status_order=1,
                                        telegram_id=callback.message.chat.id,
                                        id_order=id_order)
    await callback.message.answer_photo(photo="AgACAgIAAxkBAAIBN2XIkzZGPflWKE9lVJfjds9WZYihAAJO2zEbczhISsV6voCB0e5GAQADAgADeQADNAQ",
                                        caption=f'Наша зона доставки.'
                                                f'Укажите ваш адрес (улица, номер дома и номер квартиры):',
                                        reply_markup=keyboard_get_location())


@router.message(F.location)
async def process_get_location(message: Message, state: FSMContext):
    logging.info(f'process_get_location: {message.chat.id}')
    lat = message.location.latitude
    lon = message.location.longitude
    if check_adress_lon_alt(lon=lon, lat=lat):
        await message.answer(text=f'Укажите ваш адрес (улица, номер дома и номер квартиры):',
                             reply_markup=keyboards_main_menu())
        await state.set_state(Form_user.adress_user)
    else:
        await message.answer(text=f'Мы доставляем только в пределах указанной зоны',
                             reply_markup=keyboards_main_menu())

#
#
@router.message(F.text, StateFilter(Form_user.adress_user))
async def get_adress_user(message: Message, state: FSMContext):
    logging.info(f'get_adress_user: {message.chat.id}')
    if check_adress(adress=message.text):
        adress = message.text
        await state.update_data(adress=adress)
        user_dict[message.chat.id] = await state.get_data()
        update_status_table_number_adress(telegram_id=message.chat.id,
                                          id_order=user_dict[message.chat.id]['register_order'],
                                          adress_order=adress)
        await message.answer(text=f'Хотите оставить комментарий к заказу?',
                             reply_markup=keyboard_pass_comment())
        await state.set_state(Form_user.comment_order)
    else:
        await message.answer(text=f'Ваш адрес вне зоны.')


@router.callback_query(F.data == 'pass_comment' )
async def press_button_pass_comment(callback: CallbackQuery, state: FSMContext, bot: Bot):
    logging.info(f'press_button_pass_comment: {callback.message.chat.id}')
    logging.info(f'get_comment_order: {callback.message.chat.id}')
    comment = 'none'
    await state.update_data(comment=comment)
    update_status_table_number_comment(telegram_id=callback.message.chat.id,
                                       id_order=user_dict[callback.message.chat.id]['register_order'],
                                       comment=comment)
    await callback.message.answer(text=f'Ваш заказ уже готовят и скоро курьер его привезет.\n'
                                       f'Спасибо, что выбрали нас.\n\n'
                                       f'Вы всегда можете связаться с нами по тел. +79112972946\n\n'
                                       f'Ваша команда Шаверград!')
    list_manager = select_all_manager('manager')
    list_cook = select_all_manager('cook')
    info_user = select_row_table_users(callback.message.chat.id)
    text_manager = f'Информация о заказе:\nНаименование блюда x количество порций'

    text_cook = f'Информация о заказе:\nНаименование блюда x количество порций'

    for id_telegram_cook in list_cook:
        await bot.send_message(chat_id=id_telegram_cook,
                               text=text_cook)

    for id_telegram_manager in list_manager:
        user = get_telegram_user(id_telegram_manager, config.tg_bot.token)
        if 'result' in user:
            last_number_orders = select_row_table_number_order(callback.message.chat.id)[-1]
            order_id = last_number_orders[1]
            print('order_id', order_id)
            info_dish_last_order = select_data_table_orders_to_order_id(order_id=order_id)
            name = ''
            total = 0
            for i, info_order in enumerate(info_dish_last_order):
                info_dish = select_row_id_dish(info_order[3])
                name = name + f'{i + 1}. {info_dish[1]}: {info_dish[2]} x {info_order[4]} = {info_dish[2] * info_order[4]}руб.\n'
                total += info_dish[2] * info_order[4]
            print(id_telegram_manager)
            idorder = select_id_number_order(order_id)
            await bot.send_message(chat_id=id_telegram_manager,
                                   text=f'Номер заказа: {idorder[0]}\n'
                                        f'{name}\n\n'
                                        f'Сумма заказа: {total} руб.\n\n'
                                        f'Комментарий: {comment}\n'
                                        f'Адрес доставки: {user_dict[callback.message.chat.id]["adress"]}\n'
                                        f'Имя:{info_user[2]}\n'
                                        f'Телефон: {info_user[3]}')
        else:
            await bot.send_message(chat_id=config.tg_bot.admin_ids,
                                   text=f"Сообщение пользователю c id: {id_telegram_manager} не доставлено")

    await state.set_state(default_state)
    update_status_table_number_id_order(status_order=2,
                                        telegram_id=callback.message.chat.id,
                                        id_order=order_id)
#
@router.message(F.text, StateFilter(Form_user.comment_order))
async def get_comment_order(message: Message, state: FSMContext, bot: Bot):
    logging.info(f'get_comment_order: {message.chat.id}')
    comment = message.text
    await state.update_data(comment=comment)
    update_status_table_number_comment(telegram_id=message.chat.id,
                                       id_order=user_dict[message.chat.id]['register_order'],
                                       comment=comment)
    await message.answer(text=f'Ваш заказ уже готовят и скоро курьер его привезет.\n'
                              f'Спасибо, что выбрали нас.\n\n'
                              f'Вы всегда можете связаться с нами по тел. +79112972946\n\n'
                              f'Ваша команда Шаверград!')

    list_manager = select_all_manager('manager')
    list_cook = select_all_manager('cook')
    info_user = select_row_table_users(message.chat.id)
    text_manager = f'Информация о заказе:\nНаименование блюда x количество порций'
    call_to_phone()
    text_cook = f'Информация о заказе:\nНаименование блюда x количество порций'

    for id_telegram_cook in list_cook:
        await bot.send_message(chat_id=id_telegram_cook,
                               text=text_cook)

    for id_telegram_manager in list_manager:
        user = get_telegram_user(id_telegram_manager, config.tg_bot.token)
        if 'result' in user:
            last_number_orders = select_row_table_number_order(message.chat.id)[-1]
            order_id = last_number_orders[1]
            print('order_id', order_id)
            info_dish_last_order = select_data_table_orders_to_order_id(order_id=order_id)
            name = ''
            total = 0
            for i, info_order in enumerate(info_dish_last_order):
                info_dish = select_row_id_dish(info_order[3])
                name = name + f'{i + 1}. {info_dish[1]}: {info_dish[2]} x {info_order[4]} = {info_dish[2] * info_order[4]}руб.\n'
                total += info_dish[2] * info_order[4]
            print(id_telegram_manager)
            idorder = select_id_number_order(order_id)
            await bot.send_message(chat_id=id_telegram_manager,
                                   text=f'Номер заказа: {idorder[0]}\n'
                                        f'{name}\n\n'
                                        f'Сумма заказа: {total} руб.\n\n'
                                        f'Комментарий: {comment}\n'
                                        f'Адрес доставки: {user_dict[message.chat.id]["adress"]}\n'
                                        f'Имя:{info_user[2]}\n'
                                        f'Телефон: {info_user[3]}')
        else:
            await bot.send_message(chat_id=config.tg_bot.admin_ids,
                                   text=f"Сообщение пользователю c id: {id_telegram_manager} не доставлено")
    await state.set_state(default_state)

# ИЗМЕНЕНИЕ СОЗДАННОГО ЗАКАЗА
@router.callback_query(F.data.startswith('registerchange'))
async def press_button_register_change(callback: CallbackQuery, state: FSMContext):
    logging.info(f'press_button_register_change: {callback.message.chat.id}')
    id_order = callback.data.split('.')[1]
    await state.update_data(register_order=id_order)
    print("id_order-change", id_order)
    print('all', select_data_table_orders())
    print('id_order', select_data_table_orders_to_order_id(id_order))
    # получаем список из таблицы заказов по его id
    info_dish_last_order = select_data_table_orders_to_order_id(order_id=id_order)
    await state.update_data(list_dish_in_order=info_dish_last_order)
    await state.update_data(number_dish=0)
    print(info_dish_last_order)
    # выводим первое блюдо в заказе
    number_dish = 0
    info_order = info_dish_last_order[number_dish]
    # id первого блюда в заказе
    id_dish = info_order[3]
    # информация о блюде по его id
    info_dish = select_row_id_dish(id_dish)
    await callback.message.answer_photo(photo=info_dish[5],
                                        caption=f'<b>{info_dish[1]}</b>\n'
                                                f'Состав: {info_dish[4]}\n'
                                                f'Стоимость: {info_dish[2]} руб.\n',
                                        reply_markup=keyboard_change_order(portion=info_order[4]))


@router.callback_query(F.data.startswith('done_change'))
async def press_button_done_change(callback: CallbackQuery, state: FSMContext):
    logging.info(f'press_button_register_change: {callback.message.chat.id}')
    print('press_button_register_change')
    await press_button_register_order1(callback)


@router.callback_query(or_f(F.data == 'back_dish', F.data == 'forward_dish'))
async def press_button_done_change(callback: CallbackQuery, state: FSMContext):
    logging.info(f'press_button_done_change: {callback.message.chat.id}')
    user_dict[callback.message.chat.id] = await state.get_data()
    list_dish_in_order = user_dict[callback.message.chat.id]['list_dish_in_order']
    count_dish = len(list_dish_in_order)
    print("count_dish", count_dish)
    number_dish = user_dict[callback.message.chat.id]['number_dish']
    print("number_dish", number_dish)
    if callback.data == 'back_dish':
        print('back_dish')
        if number_dish > 0:
            number_dish -= 1
    elif callback.data == 'forward_dish':
        print('forward_dish')
        if number_dish < count_dish-1:
            number_dish += 1
    await state.update_data(number_dish=number_dish)
    info_order = list_dish_in_order[number_dish]
    id_dish = info_order[3]
    info_dish = select_row_id_dish(id_dish)
    await callback.message.answer_photo(photo=info_dish[5],
                                        caption=f'<b>{info_dish[1]}</b>\n'
                                                f'Состав: {info_dish[4]}\n'
                                                f'Стоимость: {info_dish[2]} руб.\n',
                                        reply_markup=keyboard_change_order(portion=info_order[4]))


@router.callback_query(or_f(F.data.startswith('minus_portion_edit'), F.data.startswith('plus_portion_edit')))
async def press_button_done_change(callback: CallbackQuery, state: FSMContext):
    user_dict[callback.message.chat.id] = await state.get_data()
    list_dish_in_order = user_dict[callback.message.chat.id]['list_dish_in_order']
    number_dish = user_dict[callback.message.chat.id]['number_dish']
    info_order = list_dish_in_order[number_dish]
    id_dish = info_order[3]
    order_id = info_order[2]
    portion = select_data_table_orders_idorder_iddish(telegram_id=callback.message.chat.id,
                                                      order_id=order_id,
                                                      dish_id=id_dish)[0][0]
    print('portion', portion)
    if 'minus_portion_' in callback.data:
        print('minus_portion_')
        portion = portion - 1
    elif 'plus_portion_' in callback.data:
        print('plus_portion_')
        portion = portion + 1

    if portion > 0:
        # обновляем количество порций
        update_table_orders(telegram_id=callback.message.chat.id,
                            dish_id=id_dish,
                            order_id=order_id,
                            portion=portion)
        print('portion', portion)
        # обновляем информацию о списке блюд в заказе
        info_dish_last_order = select_data_table_orders_to_order_id(order_id=order_id)

        print(info_dish_last_order)
        await state.update_data(list_dish_in_order=info_dish_last_order)
        list_dish_in_order = user_dict[callback.message.chat.id]['list_dish_in_order']
        print(list_dish_in_order)
        info_order = info_dish_last_order[number_dish]
        print(info_order)
        # for order in info_dish_last_order:
        #     if order[3] == id_dish:
        #         info_order = order

        info_dish = select_row_id_dish(id_dish)
        await callback.message.edit_caption(photo=info_dish[5],
                                            caption=f'<b>{info_dish[1]}</b>\n'
                                                    f'Состав: {info_dish[4]}\n'
                                                    f'Стоимость: {info_dish[2]} руб.\n',
                                            reply_markup=keyboard_change_order(portion=info_order[4]))
    else:
        print('portion<1')
        delete_table_orders(dish_id=id_dish,
                            order_id=order_id)
        info_dish_last_order = select_data_table_orders_to_order_id(order_id=order_id)
        print(info_dish_last_order)
        await state.update_data(list_dish_in_order=info_dish_last_order)
        # list_dish_in_order = user_dict[callback.message.chat.id]['list_dish_in_order']
        try:
            number_dish = 0
            info_order = info_dish_last_order[number_dish]
            await state.update_data(number_dish=number_dish)
            info_dish = select_row_id_dish(info_order[3])
            await callback.message.answer_photo(photo=info_dish[5],
                                                caption=f'<b>{info_dish[1]}</b>\n'
                                                        f'Состав: {info_dish[4]}\n'
                                                        f'Стоимость: {info_dish[2]} руб.\n',
                                                reply_markup=keyboard_change_order(portion=info_order[4]))
        except:
            list_category = select_all_category_table_dish()
            keyboard = keyboards_list_category(list_category)
            await callback.message.answer(text=f"Блюдо отменено. Продолжите выбор блюд 👇",
                                          reply_markup=keyboard)

@router.message(F.text == '🛒 Корзина')
async def press_button_cart(message: Message):
    logging.info(f"press_button_cart, {len(select_row_table_number_order(message.chat.id))}")
    rrr = select_row_table_number_order(message.chat.id)
    print(rrr)
    if select_row_table_number_order(message.chat.id):
        last_number_orders=select_row_table_number_order(message.chat.id)[-1]
        order_id = last_number_orders[1]
        print('order_id', order_id)
        info_dish_last_order = select_data_table_orders_to_order_id(order_id=order_id)
        name = ''
        total = 0
        for i, info_order in enumerate(info_dish_last_order):
            info_dish = select_row_id_dish(info_order[3])
            name = name + f'{i + 1}. {info_dish[1]}: {info_dish[2]} x {info_order[4]} = {info_dish[2] * info_order[4]}руб.\n'
            total += info_dish[2] * info_order[4]
        idorder = select_id_number_order(order_id)
        if total > 600:
            await message.answer(text=f'Номер заказа: {idorder[0]}\n'
                                      f'{name}\n\n'
                                      f'Сумма заказа: {total} руб.',
                                 reply_markup=keyboard_confirm_register(order_id))
        else:
            await message.answer(text=f'Номер заказа: {idorder[0]}\n'
                                      f'{name}\n\n'
                                      f'Сумма заказа: {total} руб.'
                                      f'\n\n'
                                      f'Минимальная сумма заказа 600 руб.')
    else:
        await message.answer(text='Вы еще ничего не добавили в корзину. Выберите раздел для осуществления заказа!')