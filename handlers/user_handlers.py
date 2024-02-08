from aiogram import Router, F, Bot
import logging
import datetime
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
    update_status_table_number_comment, select_all_manager, select_data_table_orders
from keyboards.keyboards_user import keyboard_confirm_phone, keyboards_get_phone, keyboards_main_menu,\
    keyboards_list_category, keyboard_paydish, keyboards_list_category_nav, keyboard_select_portion, \
    keyboard_continue_register, keyboard_confirm_register, keyboard_change_order

router = Router()
config: Config = load_config()


class Form_user(StatesGroup):
    name_user = State()
    phone_user = State()
    adress_user = State()
    comment_order = State()

user_dict = {}


@router.message(or_f(CommandStart(), and_f(lambda message:  message.text == '/user', lambda message: str(message.chat.id) == str(config.tg_bot.admin_ids))))
async def process_start_command_user(message: Message, state: FSMContext) -> None:
    logging.info(f'process_start_command_admin: {message.chat.id}')
    create_table_user()
    await message.answer(text=f"""Друзья, всем доброго времени суток, рады будем вас накормить вкуснейшей шавермой и мощнейшими бургерами у нас в "Шаверграде" по адресу: Вишерская улица 2
график работы: 10:00-23:00 без перерывов и выходных""")
    row_user = select_row_table_users(message.chat.id)
    # print(row_user)
    if not row_user:
        await message.answer(text='Как вас зовут?')
        await state.set_state(Form_user.name_user)
    else:
        await message.answer(text=f'Рады видеть вас снова {row_user[2]}\n'
                                  f'телефон: {row_user[3]}',
                             reply_markup=keyboard_confirm_phone())


@router.message(F.text, StateFilter(Form_user.name_user))
async def get_name_user(message: Message, state: FSMContext) -> None:
    await state.update_data(user_name=message.text)
    await message.answer(text='Укажи свой телефон',
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
    await callback.message.answer(text='Выберите раздел',
                                  reply_markup=keyboards_main_menu())
    await state.set_state(default_state)


@router.message(StateFilter(Form_user.phone_user))
async def get_phone_user(message: Message, state: FSMContext) -> None:
    if message.contact:
        phone = str(message.contact.phone_number)
        # print(phone)
    else:
        phone = message.text
    await state.update_data(user_phone=phone)
    user_dict[message.chat.id] = await state.get_data()
    insert_data_table_users(telegram_id=message.chat.id,
                            name=user_dict[message.chat.id]['user_name'],
                            phone=user_dict[message.chat.id]['user_phone'])
    await message.answer(text="""С помощью нашего бота-помощника вы можете ознакомиться с нашим меню, сделать онлайн заказ и наши курьеры доставят вам его. Кроме того в разделе акции вы узнаете о самых актуальных акциях!""")
    await message.answer(text='Выберите раздел',
                         reply_markup=keyboards_main_menu())
    await state.set_state(default_state)


@router.message(F.text == '🏠')
async def press_button_home(message: Message):
    await message.answer(text='Выберите раздел',
                         reply_markup=keyboards_main_menu())


@router.message(F.text == 'Контакты 📞')
async def press_button_contact(message: Message):
    await message.answer_photo(photo='AgACAgIAAxkBAAINfGXCj50djUS5cRqccZuZT4JUTApwAAKU1zEbIZEQShVaSuyyAaIVAQADAgADeAADNAQ',
                               caption="""К сожалению в Яндекс картах нас пока нет, но мы это исправляем! Ориентир: внешняя часть угла дома

10:00-23:00 без перерывов и выходных
Вишерская улица 2""")


@router.message(F.text == 'Акции')
async def press_button_promotion(message: Message):
    list_promotion = select_all_data_table_promotion()
    for promo in list_promotion:
        # print(promo)
        if promo[2] != 'none':
            await message.answer_photo(photo=promo[2],
                                       caption=promo[1])
        else:
            await message.answer(text=promo[1])


@router.message(F.text == 'Меню 🍴')
async def press_button_menu(message: Message):
    list_category = select_all_category_table_dish()
    keyboard = keyboards_list_category(list_category)
    await message.answer(text=f"""Минимальная сумма заказа: <b>1700р.</b>
Прием заказов осуществляется с 10:00 до 22:45

Выбери раздел:""",
                         reply_markup=keyboard)


@router.message(F.text.in_(select_all_category_table_dish()))
async def press_button_category(message: Message, state: FSMContext):
    """
    Функция получает наименование категории блюда и формирует три карточки из этой категории
    :param message: категория
    :param state:
    :return: выводит три карточки блюд
    """
    logging.info(f'press_button_category: {message.chat.id}')
    category = message.text
    await state.update_data(select_category=category)
    await state.update_data(num_block=1)
    list_id_dish_category = select_dish_in_category(category)
    # print(list_id_dish_category)
    back = 0
    forward = 2
    count = 3

    len_list = len(list_id_dish_category)
    int_block = len_list // count
    remain_block = len_list % count
    if remain_block:
        int_block += 1
    for id_dish in list_id_dish_category[back*count:(forward-1)*count]:
        # print('id_dish', id_dish)
        row_dish = select_row_id_dish(id_dish[0])
        # print('row_dish', row_dish)
        # если не в стоп листе
        if not row_dish[-1]:
            await message.answer_photo(photo=row_dish[-2],
                                       caption=f'Название: {row_dish[1]}'
                                               f'Описание: {row_dish[4]}',
                                       reply_markup=keyboard_paydish(row_dish[2], row_dish[0]))
    list_category = select_all_category_table_dish()
    await message.answer(text="Закажите блюдо",
                         reply_markup=keyboards_list_category_nav(list_category))


@router.message(or_f(F.text == '<< Назад', F.text == 'Вперед >>'))
async def press_button_back_forward(message: Message, state: FSMContext):
    """
    Функция реагирует на нажатие на кнопки навигации - << Назад и Вперед >> увеличивая
    номер выводимо блока с карточками блюд
    :param message:
    :param state:
    :return:
    """
    logging.info(f'press_button_back_forward: {message.chat.id}')
    user_dict[message.chat.id] = await state.get_data()
    category = user_dict[message.chat.id]['select_category']
    num_block = user_dict[message.chat.id]['num_block']
    print("num_block", num_block)
    list_id_dish_category = select_dish_in_category(category)
    print(list_id_dish_category)
    count = 3
    len_list = len(list_id_dish_category)
    int_block = len_list // count
    remain_block = len_list % count
    if remain_block:
        int_block += 1
    print('int_block: ', int_block)
    back = 0
    forward = 1
    if message.text == '<< Назад':
        num_block -= 1
        if num_block == 1:
            back = 0
            forward = 2
            await state.update_data(num_block=back+1)
        else:
            back = num_block - 1
            forward = num_block + 1
            await state.update_data(num_block=back+1)
    elif message.text == 'Вперед >>':
        num_block += 1
        if num_block == int_block:
            back = int_block - 1
            forward = int_block + 1
            await state.update_data(num_block=back+1)
        else:
            back = num_block - 1
            forward = num_block + 1
            await state.update_data(num_block=back+1)

    print('back:', back, 'forward:', forward)
    for id_dish in list_id_dish_category[back*count:(forward-1)*count]:
        # print('id_dish', id_dish)
        row_dish = select_row_id_dish(id_dish[0])
        # print('row_dish', row_dish)
        # если не в стоп листе
        if not row_dish[-1]:
            await message.answer_photo(photo=row_dish[-2],
                                       caption=f'Название: {row_dish[1]}'
                                               f'Описание: {row_dish[4]}',
                                       reply_markup=keyboard_paydish(row_dish[2], row_dish[0]))
    list_category = select_all_category_table_dish()
    await message.answer(text="Закажите блюдо",
                         reply_markup=keyboards_list_category_nav(list_category))


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
    await callback.message.answer(text=f'Вы выбрали'
                                       f'{info_dish[1]}',
                                  reply_markup=keyboards_list_category(list_category))
    await callback.message.answer(text=f'Укажите количество порций!',
                                  reply_markup=keyboard_select_portion(portion=portion_old[0][0]))


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
        await callback.message.edit_text(text=f'Укажите количество порций!',
                                         reply_markup=keyboard_select_portion(portion=portion))
    except:
        await callback.message.edit_text(text=f'Укажитe количество порций!',
                                         reply_markup=keyboard_select_portion(portion=portion))


@router.callback_query(F.data == 'order_dish')
async def press_button_order_dish(callback: CallbackQuery, state: FSMContext):
    logging.info(f'press_button_order_dish: {callback.message.chat.id}')
    user_dict[callback.message.chat.id] = await state.get_data()
    update_table_orders(telegram_id=callback.message.chat.id,
                        dish_id=user_dict[callback.message.chat.id]['id_dish'],
                        order_id=user_dict[callback.message.chat.id]['id_order'],
                        portion=user_dict[callback.message.chat.id]['portion'])
    await callback.message.answer(text='Желаете что то добавить в свой заказ?',
                                  reply_markup=keyboard_continue_register())


@router.callback_query(F.data == 'cancel_order_dish')
async def press_button_cancel_order_dish(callback: CallbackQuery, state: FSMContext):
    logging.info(f'press_button_cancel_order_dish: {callback.message.chat.id}')
    list_category = select_all_category_table_dish()
    keyboard = keyboards_list_category(list_category)
    await callback.message.answer(text=f"""Минимальная сумма заказа: <b>1700р.</b>
    Прием заказов осуществляется с 10:00 до 22:45

    Выбери раздел:""",
                                  reply_markup=keyboard)


@router.callback_query(F.data == 'continue_order')
async def press_button_continue_order(callback: CallbackQuery, state: FSMContext):
    logging.info(f'press_button_continue_order: {callback.message.chat.id}')
    list_category = select_all_category_table_dish()
    keyboard = keyboards_list_category(list_category)
    await callback.message.answer(text=f"""Минимальная сумма заказа: <b>1700р.</b>
    Прием заказов осуществляется с 10:00 до 22:45

    Выбери раздел:""",
                                  reply_markup=keyboard)


@router.callback_query(F.data == 'register_order')
async def press_button_register_order(callback: CallbackQuery):
    logging.info(f'press_button_register_order: {callback.message.chat.id}')
    print('press_button_register_order')
    last_number_orders = select_row_table_number_order(callback.message.chat.id)[-1]
    if last_number_orders[-1] == 0:
        order_id = last_number_orders[1]
        print('order_id', order_id)
        info_dish_last_order = select_data_table_orders_to_order_id(order_id=order_id)
        name = ''
        total = 0
        for i, info_order in enumerate(info_dish_last_order):
            info_dish = select_row_id_dish(info_order[3])
            name = name+f'{i+1}. {info_dish[1]}: {info_dish[2]} x {info_order[4]} = {info_dish[2] * info_order[4]}руб.\n'
            total += info_dish[2]*info_order[4]
        await callback.message.answer(text=f'{name}\n\n'
                                           f'Сумма заказа: {total} руб.',
                                      reply_markup=keyboard_confirm_register(order_id))


@router.callback_query(F.data.startswith('registerdone'))
async def press_button_register_all_done(callback: CallbackQuery, state: FSMContext):
    logging.info(f'press_button_register_all_done: {callback.message.chat.id}')
    print('press_button_register_all_done')
    id_order = callback.data.split('.')[1]
    print('id_order-done', id_order)
    await state.update_data(register_order=id_order)
    update_status_table_number_id_order(telegram_id=callback.message.chat.id,
                                        id_order=id_order)
    await callback.message.answer(text=f'Укажите ваш адрес.')
    await state.set_state(Form_user.adress_user)


@router.message(F.text, StateFilter(Form_user.adress_user))
async def get_adress_user(message: Message, state: FSMContext):
    logging.info(f'get_adress_user: {message.chat.id}')
    adress = message.text
    user_dict[message.chat.id] = await state.get_data()
    update_status_table_number_adress(telegram_id=message.chat.id,
                                      id_order=user_dict[message.chat.id]['register_order'],
                                      adress_order=adress)
    await message.answer(text=f'Оставьте комментарий к заказу!')
    await state.set_state(Form_user.comment_order)


@router.message(F.text, StateFilter(Form_user.comment_order))
async def get_comment_order(message: Message, state: FSMContext, bot: Bot):
    logging.info(f'get_comment_order: {message.chat.id}')
    comment = message.text
    update_status_table_number_comment(telegram_id=message.chat.id,
                                       id_order=user_dict[message.chat.id]['register_order'],
                                       comment=comment)
    await message.answer(text=f'Ваш заказ уже готовят и скоро курьер его привезет! Спасибо что выбрали нас')
    list_manager = select_all_manager('manager')
    list_cook = select_all_manager('cook')

    text_manager = f'Информация о заказе:\nНаименование блюда x количество порций'

    text_cook = f'Информация о заказе:\nНаименование блюда x количество порций'

    for id_telegram_cook in list_cook:
        await bot.send_message(chat_id=id_telegram_cook,
                               text=text_cook)

    for id_telegram_manager in list_manager:
        await bot.send_message(chat_id=id_telegram_manager,
                               text=text_manager)


@router.callback_query(F.data.startswith('registerchange'))
async def press_button_register_change(callback: CallbackQuery, state: FSMContext):
    logging.info(f'press_button_register_change: {callback.message.chat.id}')
    print('press_button_register_change')
    id_order = callback.data.split('.')[1]
    print("id_order-change", id_order)
    print('all', select_data_table_orders())
    print('id_order', select_data_table_orders_to_order_id(id_order))
    info_dish_last_order = select_data_table_orders_to_order_id(order_id=id_order)
    await state.update_data(list_dish_in_order=info_dish_last_order)
    await state.update_data(number_dish=1)
    print(info_dish_last_order)
    number_dish = 1
    info_order = info_dish_last_order[number_dish-1]
    id_dish = info_order[3]
    info_dish = select_row_id_dish(id_dish)
    await callback.message.answer_photo(photo=info_dish[5],
                                        caption=f'{info_dish[1]}\n'
                                                f'{info_dish[4]}\n'
                                                f'{info_dish[2]}\n',
                                        reply_markup=keyboard_change_order(number_dish))


@router.callback_query(F.data.startswith('done_change'))
async def press_button_done_change(callback: CallbackQuery, state: FSMContext):
    logging.info(f'press_button_register_change: {callback.message.chat.id}')
    print('press_button_register_change')
    await press_button_register_order(callback)


@router.callback_query(or_f(F.data == 'back_dish', F.data == 'forward_dish'))
async def press_button_done_change(callback: CallbackQuery, state: FSMContext):
    user_dict[callback.message.chat.id] = await state.get_data()
    list_dish_in_order = user_dict[callback.message.chat.id]['list_dish_in_order']
    count_dish = len(list_dish_in_order)
    number_dish = user_dict[callback.message.chat.id]['number_dish']

    if callback.data == 'back_dish':
        if number_dish > 1:
            number_dish -= 1
    elif callback.data == 'forward_dish':
        if number_dish < count_dish:
            number_dish += 1
    info_order = list_dish_in_order[number_dish - 1]
    id_dish = info_order[3]
    info_dish = select_row_id_dish(id_dish)
    await callback.message.answer_photo(photo=info_dish[5],
                                        caption=f'{info_dish[1]}\n'
                                                f'{info_dish[4]}\n'
                                                f'{info_dish[2]}\n',
                                        reply_markup=keyboard_change_order(number_dish))


@router.message(F.text == 'Корзина 🛒')
async def press_button_cart(message: Message):
    print("press_button_cart")
    last_number_orders = select_row_table_number_order(message.chat.id)[-1]
    if last_number_orders[-1] == 0:
        order_id = last_number_orders[1]
        print('order_id', order_id)
        info_dish_last_order = select_data_table_orders_to_order_id(order_id=order_id)
        name = ''
        total = 0
        for i, info_order in enumerate(info_dish_last_order):
            info_dish = select_row_id_dish(info_order[3])
            name = name + f'{i + 1}. {info_dish[1]}: {info_dish[2]} x {info_order[4]} = {info_dish[2] * info_order[4]}руб.\n'
            total += info_dish[2] * info_order[4]
        await message.answer(text=f'{name}\n\n'
                                           f'Сумма заказа: {total} руб.',
                                      reply_markup=keyboard_confirm_register(order_id))
    else:
        await message.answer(text='Вы еще ничего не добавили в корзину. Выберите раздел для осуществления заказа!')