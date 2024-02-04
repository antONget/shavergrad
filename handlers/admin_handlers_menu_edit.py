from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter

from config_data.config import Config, load_config
from module.database import select_all_data_table_dish, select_dish_in_category, select_row_id_dish, update_field_table_dish
from keyboards.keyboards_admin import keyboards_select_dish_edit_menu, keyboard_edit_attribute_dish, keyboard_back, keyboard_edit_menu
import logging

router = Router()
config: Config = load_config()


class Dish_edit(StatesGroup):
    edit_name_dish = State()
    edit_description_dish = State()
    edit_photo_dish = State()
    edit_cost_dish = State()
    edit_category_dish = State()


user_dict = {}


@router.callback_query(F.data == 'edit_dish')
async def press_button_edit_dish_setting(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'press_button_edit_dish_setting: {callback.message.chat.id}')
    all_data_table_dish = select_all_data_table_dish()
    list_category_dish_table_dish = [row[3] for row in all_data_table_dish]
    set_category_dish_table_dish = set(list_category_dish_table_dish)
    list_category_dish_table_dish = list(set_category_dish_table_dish)
    # id_dish_table_dish = [row[1] for row in all_data_table_dish]
    back = 0
    forward = 2
    count_item = 6
    keyboard = keyboards_select_dish_edit_menu(list_data_button=list_category_dish_table_dish,
                                               list_id_callback=list_category_dish_table_dish,
                                               back=back,
                                               forward=forward,
                                               count=count_item,
                                               str_callback_button='editdish')
    await callback.message.answer(text=f'Выберите категорию в которой вы хотите отредактировать карточку блюда',
                                  reply_markup=keyboard)


# >>>>
@router.callback_query(F.data.startswith('editdishforward'))
async def press_button_edit_dish_setting_forward(callback: CallbackQuery) -> None:
    logging.info(f'press_button_edit_dish_setting_forward: {callback.message.chat.id}')
    all_data_table_dish = select_all_data_table_dish()
    list_category_dish_table_dish = [row[3] for row in all_data_table_dish]
    set_category_dish_table_dish = set(list_category_dish_table_dish)
    list_category_dish_table_dish = list(set_category_dish_table_dish)
    forward = int(callback.data.split('_')[1]) + 1
    back = forward - 2
    count_item = 6
    keyboard = keyboards_select_dish_edit_menu(list_data_button=list_category_dish_table_dish,
                                               list_id_callback=list_category_dish_table_dish,
                                               back=back,
                                               forward=forward,
                                               count=count_item,
                                               str_callback_button='editdish')
    try:
        await callback.message.edit_text(text=f'Выберите категорию в которой вы хотите отредактировать карточку блюда',
                                         reply_markup=keyboard)
    except:
        await callback.message.edit_text(text=f'Выберите категорию в которой вы хотите отрeдактировать карточку блюда',
                                         reply_markup=keyboard)


# <<<<
@router.callback_query(F.data.startswith('editdishback'))
async def press_button_edit_dish_setting_back(callback: CallbackQuery) -> None:
    logging.info(f'press_button_edit_dish_setting_back: {callback.message.chat.id}')
    all_data_table_dish = select_all_data_table_dish()
    list_category_dish_table_dish = [row[3] for row in all_data_table_dish]
    set_category_dish_table_dish = set(list_category_dish_table_dish)
    list_category_dish_table_dish = list(set_category_dish_table_dish)
    back = int(callback.data.split('_')[1]) - 1
    forward = back + 2
    count_item = 6
    keyboard = keyboards_select_dish_edit_menu(list_data_button=list_category_dish_table_dish,
                                               list_id_callback=list_category_dish_table_dish,
                                               back=back,
                                               forward=forward,
                                               count=count_item,
                                               str_callback_button='editdish')
    try:
        await callback.message.edit_text(text=f'Выберите категорию в которой вы хотите отредактировать карточку блюда',
                                         reply_markup=keyboard)
    except:
        await callback.message.edit_text(text=f'Выберите категорию в которой вы хотите отрeдактировать карточку блюда',
                                         reply_markup=keyboard)

# МЕНЮ - Редактировать - Категории - Блюда
@router.callback_query(F.data.startswith('editdishtextbutton'))
async def press_button_select_dish_edit_dish_setting(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'press_button_select_dish_edit_dish_setting: {callback.message.chat.id}')
    category_dish = callback.data.split('_')[1]
    print(category_dish)
    await state.update_data(select_edit_dish_category=category_dish)
    list_dish_in_category = select_dish_in_category(category_dish)
    list_data_button = [row[1] for row in list_dish_in_category]
    list_id_callback = [row[0] for row in list_dish_in_category]
    back = 0
    forward = 2
    count_item = 6
    keyboard = keyboards_select_dish_edit_menu(list_data_button=list_data_button,
                                               list_id_callback=list_id_callback,
                                               back=back,
                                               forward=forward,
                                               count=count_item,
                                               str_callback_button='editdishselect')
    await callback.message.answer(text=f'Выберите блюдо котороe вы хотите отредактировать',
                                  reply_markup=keyboard)


# >>>>
@router.callback_query(F.data.startswith('editdishselectforward'))
async def press_button_select_dish_edit_dish_setting_forward(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'press_button_select_dish_edit_dish_setting_forward: {callback.message.chat.id}')
    user_dict[callback.message.chat.id] = await state.get_data()
    print(user_dict[callback.message.chat.id])
    category_dish = user_dict[callback.message.chat.id]['select_edit_dish_category']
    list_dish_in_category = select_dish_in_category(category_dish)
    print(list_dish_in_category)
    list_data_button = [row[1] for row in list_dish_in_category]
    list_id_callback = [row[0] for row in list_dish_in_category]
    forward = int(callback.data.split('_')[1]) + 1
    back = forward - 2
    count_item = 6
    keyboard = keyboards_select_dish_edit_menu(list_data_button=list_data_button,
                                               list_id_callback=list_id_callback,
                                               back=back,
                                               forward=forward,
                                               count=count_item,
                                               str_callback_button='editdishselect')
    try:
        await callback.message.edit_text(text=f'Выберите блюдо, которое вы хотите отредактировать',
                                         reply_markup=keyboard)
    except:
        await callback.message.edit_text(text=f'Выберите блюдо, котороe вы хотите отредактировать',
                                         reply_markup=keyboard)


# <<<<
@router.callback_query(F.data.startswith('editdishselectback'))
async def press_button_select_dish_edit_dish_setting_back(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'press_button_select_dish_edit_dish_setting_back: {callback.message.chat.id}')
    user_dict[callback.message.chat.id] = await state.get_data()
    category_dish = user_dict[callback.message.chat.id]['select_edit_dish_category']
    list_dish_in_category = select_dish_in_category(category_dish)
    list_data_button = [row[1] for row in list_dish_in_category]
    list_id_callback = [row[0] for row in list_dish_in_category]
    back = int(callback.data.split('_')[1]) - 1
    forward = back + 2
    count_item = 6
    keyboard = keyboards_select_dish_edit_menu(list_data_button=list_data_button,
                                               list_id_callback=list_id_callback,
                                               back=back,
                                               forward=forward,
                                               count=count_item,
                                               str_callback_button='editdishselect')
    try:
        await callback.message.edit_text(text=f'Выберите блюдо, которое вы хотите отредактировать',
                                         reply_markup=keyboard)
    except:
        await callback.message.edit_text(text=f'Выберите блюдо, котороe вы хотите отредактировать',
                                         reply_markup=keyboard)


# МЕНЮ - Редактировать - Категория - Блюда - Выбор атрибута для редактирования
@router.callback_query(F.data.startswith('editdishselecttextbutton'))
async def press_button_select_dish_edit_attribute_setting(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'press_button_select_dish_edit_attribute_setting: {callback.message.chat.id}')
    id_dish = callback.data.split('_')[1]
    await state.update_data(select_edit_dish=id_dish)
    data_id_dish = select_row_id_dish(id_dish)
    print(data_id_dish)
    keyboard = keyboard_edit_attribute_dish(data_id_dish[-1])
    if data_id_dish[-1]:
        is_stop = 'Выведено из меню'
    else:
        is_stop = 'Можно заказать'
    await callback.message.answer_photo(photo=data_id_dish[5],
                                        caption=f"Категория блюда: {data_id_dish[3]}\n"
                                                f"Наименование блюда: {data_id_dish[1]}\n"
                                                f"Описание блюда: {data_id_dish[4]}\n"
                                                f"Стоимость блюда: {data_id_dish[2]}\n"
                                                f"Можно заказать: {is_stop}\n\n"
                                                f"Что вы хотите исправить?",
                                        reply_markup=keyboard)


# МЕНЮ - Редактировать - Категория - Блюда - Выбор атрибута для редактирования - Стоп-лист
@router.callback_query(F.data == 'edit_attribute_is_stop')
async def press_button_edit_attribute_is_stop(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'press_button_edit_attribute_is_stop: {callback.message.chat.id}')
    user_dict[callback.message.chat.id] = await state.get_data()
    id_dish = user_dict[callback.message.chat.id]['select_edit_dish']
    data_id_dish = select_row_id_dish(id_dish)
    if data_id_dish[-1]:
        update_field_table_dish('is_stop', 0, id_dish)
    else:
        update_field_table_dish('is_stop', 1, id_dish)
    if data_id_dish[-1]:
        is_stop = 'Выведено из меню'
    else:
        is_stop = 'Можно заказать'
    data_id_dish = select_row_id_dish(id_dish)
    keyboard = keyboard_edit_attribute_dish(data_id_dish[-1])
    await callback.message.answer_photo(photo=data_id_dish[5],
                                        caption=f"Категория блюда: {data_id_dish[3]}\n"
                                                f"Наименование блюда: {data_id_dish[1]}\n"
                                                f"Описание блюда: {data_id_dish[4]}\n"
                                                f"Стоимость блюда: {data_id_dish[2]}\n"
                                                f"Можно заказать: {is_stop}\n\n"
                                                f"Что вы хотите исправить?",
                                        reply_markup=keyboard)


# МЕНЮ - Редактировать - Категория - Блюда - Выбор атрибута для редактирования - Категория
@router.callback_query(F.data == 'edit_attribute_category')
async def press_button_edit_attribute_category(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'press_button_edit_attribute_category: {callback.message.chat.id}')
    await state.set_state(Dish_edit.edit_category_dish)
    await callback.message.answer(text='Отправьте новую категорию блюда',
                                  reply_markup=keyboard_back())


@router.message(F.text, StateFilter(Dish_edit.edit_category_dish))
async def get_edit_attribute_category(message: Message, state: FSMContext) -> None:
    logging.info(f'get_edit_attribute_category: {message.chat.id}')
    user_dict[message.chat.id] = await state.get_data()
    id_dish = user_dict[message.chat.id]['select_edit_dish']
    update_field_table_dish(set_field='category_dish', set_data=message.text, id_dish=id_dish)
    await state.set_state(default_state)

    data_id_dish = select_row_id_dish(id_dish)
    print(data_id_dish)
    keyboard = keyboard_edit_attribute_dish(data_id_dish[-1])
    if data_id_dish[-1]:
        is_stop = 'Выведено из меню'
    else:
        is_stop = 'Можно заказать'
    await message.answer_photo(photo=data_id_dish[5],
                               caption=f"Категория блюда: {data_id_dish[3]}\n"
                                       f"Наименование блюда: {data_id_dish[1]}\n"
                                       f"Описание блюда: {data_id_dish[4]}\n"
                                       f"Стоимость блюда: {data_id_dish[2]}\n"
                                       f"Можно заказать: {is_stop}\n\n"
                                       f"Что вы хотите исправить?",
                               reply_markup=keyboard)


# МЕНЮ - Редактировать - Категория - Блюда - Выбор атрибута для редактирования - Наименование
@router.callback_query(F.data == 'edit_attribute_name')
async def press_button_edit_attribute_name(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'press_button_edit_attribute_name: {callback.message.chat.id}')
    await state.set_state(Dish_edit.edit_name_dish)
    await callback.message.answer(text='Отправьте новое наименование блюда',
                                  reply_markup=keyboard_back())


@router.message(F.text, StateFilter(Dish_edit.edit_name_dish))
async def get_edit_attribute_name(message: Message, state: FSMContext) -> None:
    logging.info(f'get_edit_attribute_name: {message.chat.id}')
    user_dict[message.chat.id] = await state.get_data()
    id_dish = user_dict[message.chat.id]['select_edit_dish']
    update_field_table_dish(set_field='name_dish', set_data=message.text, id_dish=id_dish)
    await state.set_state(default_state)

    data_id_dish = select_row_id_dish(id_dish)
    print(data_id_dish)
    keyboard = keyboard_edit_attribute_dish(data_id_dish[-1])
    if data_id_dish[-1]:
        is_stop = 'Выведено из меню'
    else:
        is_stop = 'Можно заказать'
    await message.answer_photo(photo=data_id_dish[5],
                               caption=f"Категория блюда: {data_id_dish[3]}\n"
                                       f"Наименование блюда: {data_id_dish[1]}\n"
                                       f"Описание блюда: {data_id_dish[4]}\n"
                                       f"Стоимость блюда: {data_id_dish[2]}\n"
                                       f"Можно заказать: {is_stop}\n\n"
                                       f"Что вы хотите исправить?",
                               reply_markup=keyboard)


# МЕНЮ - Редактировать - Категория - Блюда - Выбор атрибута для редактирования - Изображение
@router.callback_query(F.data == 'edit_attribute_id_photo')
async def press_button_edit_attribute_photo(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'press_button_edit_attribute_photo: {callback.message.chat.id}')
    await state.set_state(Dish_edit.edit_photo_dish)
    await callback.message.answer(text='Отправьте новую фотографию блюда',
                                  reply_markup=keyboard_back())


@router.message(F.photo, StateFilter(Dish_edit.edit_photo_dish))
async def get_edit_attribute_photo(message: Message, state: FSMContext) -> None:
    logging.info(f'get_edit_attribute_name: {message.chat.id}')
    id_photo = message.photo[-1].file_id
    user_dict[message.chat.id] = await state.get_data()
    id_dish = user_dict[message.chat.id]['select_edit_dish']
    update_field_table_dish(set_field='picture_dish', set_data=id_photo, id_dish=id_dish)
    await state.set_state(default_state)

    data_id_dish = select_row_id_dish(id_dish)
    print(data_id_dish)
    keyboard = keyboard_edit_attribute_dish(data_id_dish[-1])
    if data_id_dish[-1]:
        is_stop = 'Выведено из меню'
    else:
        is_stop = 'Можно заказать'
    await message.answer_photo(photo=data_id_dish[5],
                               caption=f"Категория блюда: {data_id_dish[3]}\n"
                                       f"Наименование блюда: {data_id_dish[1]}\n"
                                       f"Описание блюда: {data_id_dish[4]}\n"
                                       f"Стоимость блюда: {data_id_dish[2]}\n"
                                       f"Можно заказать: {is_stop}\n\n"
                                       f"Что вы хотите исправить?",
                               reply_markup=keyboard)


# МЕНЮ - Редактировать - Категория - Блюда - Выбор атрибута для редактирования - Описание
@router.callback_query(F.data == 'edit_attribute_description')
async def press_button_edit_attribute_description(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'press_button_edit_attribute_description: {callback.message.chat.id}')
    await state.set_state(Dish_edit.edit_description_dish)
    await callback.message.answer(text='Отправьте новое описание блюда',
                                  reply_markup=keyboard_back())


@router.message(F.text, StateFilter(Dish_edit.edit_description_dish))
async def get_edit_attribute_description(message: Message, state: FSMContext) -> None:
    logging.info(f'get_edit_attribute_description: {message.chat.id}')
    user_dict[message.chat.id] = await state.get_data()
    id_dish = user_dict[message.chat.id]['select_edit_dish']
    update_field_table_dish(set_field='description_dish', set_data=message.text, id_dish=id_dish)
    await state.set_state(default_state)

    data_id_dish = select_row_id_dish(id_dish)
    print(data_id_dish)
    keyboard = keyboard_edit_attribute_dish(data_id_dish[-1])
    if data_id_dish[-1]:
        is_stop = 'Выведено из меню'
    else:
        is_stop = 'Можно заказать'
    await message.answer_photo(photo=data_id_dish[5],
                               caption=f"Категория блюда: {data_id_dish[3]}\n"
                                       f"Наименование блюда: {data_id_dish[1]}\n"
                                       f"Описание блюда: {data_id_dish[4]}\n"
                                       f"Стоимость блюда: {data_id_dish[2]}\n"
                                       f"Можно заказать: {is_stop}\n\n"
                                       f"Что вы хотите исправить?",
                               reply_markup=keyboard)


# МЕНЮ - Редактировать - Категория - Блюда - Выбор атрибута для редактирования - Стоимость
@router.callback_query(F.data == 'edit_attribute_cost')
async def press_button_edit_attribute_cost(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'press_button_edit_attribute_cost: {callback.message.chat.id}')
    await state.set_state(Dish_edit.edit_cost_dish)
    await callback.message.answer(text='Отправьте новую цену блюда',
                                  reply_markup=keyboard_back())


@router.message(F.text, StateFilter(Dish_edit.edit_cost_dish))
async def get_edit_attribute_cost(message: Message, state: FSMContext) -> None:
    logging.info(f'get_edit_attribute_cost: {message.chat.id}')
    user_dict[message.chat.id] = await state.get_data()
    id_dish = user_dict[message.chat.id]['select_edit_dish']
    update_field_table_dish(set_field='cost_dish', set_data=message.text, id_dish=id_dish)
    await state.set_state(default_state)

    data_id_dish = select_row_id_dish(id_dish)
    print(data_id_dish)
    keyboard = keyboard_edit_attribute_dish(data_id_dish[-1])
    if data_id_dish[-1]:
        is_stop = 'Выведено из меню'
    else:
        is_stop = 'Можно заказать'
    await message.answer_photo(photo=data_id_dish[5],
                               caption=f"Категория блюда: {data_id_dish[3]}\n"
                                       f"Наименование блюда: {data_id_dish[1]}\n"
                                       f"Описание блюда: {data_id_dish[4]}\n"
                                       f"Стоимость блюда: {data_id_dish[2]}\n"
                                       f"Можно заказать: {is_stop}\n\n"
                                       f"Что вы хотите исправить?",
                               reply_markup=keyboard)


@router.callback_query(F.data == 'back_edit_attribute')
async def press_button_edit_back(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'press_button_edit_back: {callback.message.chat.id}')
    await state.set_state(default_state)
    user_dict[callback.message.chat.id] = await state.get_data()
    id_dish = user_dict[callback.message.chat.id]['select_edit_dish']
    data_id_dish = select_row_id_dish(id_dish)
    print(data_id_dish)
    keyboard = keyboard_edit_attribute_dish(data_id_dish[-1])
    if data_id_dish[-1]:
        is_stop = 'Выведено из меню'
    else:
        is_stop = 'Можно заказать'
    await callback.message.answer_photo(photo=data_id_dish[5],
                                        caption=f"Категория блюда: {data_id_dish[3]}\n"
                                                f"Наименование блюда: {data_id_dish[1]}\n"
                                                f"Описание блюда: {data_id_dish[4]}\n"
                                                f"Стоимость блюда: {data_id_dish[2]}\n"
                                                f"Можно заказать: {is_stop}\n\n"
                                                f"Что вы хотите исправить?",
                                        reply_markup=keyboard)


@router.callback_query(F.data == 'edit_attribute_done')
async def press_button_edit_attribute_done(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'press_button_edit_attribute_done: {callback.message.chat.id}')
    keyboard = keyboard_edit_menu()
    await callback.message.answer(text='Выберите пункт',
                                  reply_markup=keyboard)