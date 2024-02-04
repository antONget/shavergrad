from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter

from config_data.config import Config, load_config
from module.database import select_all_data_table_dish, select_dish_in_category, select_row_id_dish,\
    update_field_table_dish, dalete_row_table_dish
from keyboards.keyboards_admin import keyboards_select_dish_edit_menu, keyboard_edit_attribute_dish, keyboard_back,\
    keyboard_edit_menu, keyboard_delete_select_dish
import logging

router = Router()
config: Config = load_config()


user_dict = {}


@router.callback_query(F.data == 'delete_dish')
async def press_button_delete_dish_setting(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'press_button_delete_dish_setting: {callback.message.chat.id}')
    all_data_table_dish = select_all_data_table_dish()
    list_category_dish_table_dish = [row[3] for row in all_data_table_dish]
    set_category_dish_table_dish = set(list_category_dish_table_dish)
    list_category_dish_table_dish = list(set_category_dish_table_dish)

    back = 0
    forward = 2
    count_item = 6
    keyboard = keyboards_select_dish_edit_menu(list_data_button=list_category_dish_table_dish,
                                               list_id_callback=list_category_dish_table_dish,
                                               back=back,
                                               forward=forward,
                                               count=count_item,
                                               str_callback_button='deletedish')
    await callback.message.answer(text=f'Выберите категорию в которой вы хотите удалить блюдо',
                                  reply_markup=keyboard)


# >>>>
@router.callback_query(F.data.startswith('deletedishforward'))
async def press_button_delete_dish_setting_forward(callback: CallbackQuery) -> None:
    logging.info(f'press_button_delete_dish_setting_forward: {callback.message.chat.id}')
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
                                               str_callback_button='deletedish')
    try:
        await callback.message.edit_text(text=f'Выберите категорию в которой вы хотите удалить карточку блюда',
                                         reply_markup=keyboard)
    except:
        await callback.message.edit_text(text=f'Выберите категорию в которой вы хотите удалить карточку блюда',
                                         reply_markup=keyboard)


# <<<<
@router.callback_query(F.data.startswith('deletedishback'))
async def press_button_delete_dish_setting_back(callback: CallbackQuery) -> None:
    logging.info(f'press_button_delete_dish_setting_back: {callback.message.chat.id}')
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
                                               str_callback_button='deletedish')
    try:
        await callback.message.edit_text(text=f'Выберите категорию в которой вы хотите удалить карточку блюда',
                                         reply_markup=keyboard)
    except:
        await callback.message.edit_text(text=f'Выберите категорию в которой вы хотите удалить карточку блюда',
                                         reply_markup=keyboard)


# МЕНЮ - Редактировать - Категории - Блюда
@router.callback_query(F.data.startswith('deletedishtextbutton'))
async def press_button_select_dish_delete_dish_setting(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'press_button_select_dish_delete_dish_setting: {callback.message.chat.id}')
    category_dish = callback.data.split('_')[1]
    print(category_dish)
    await state.update_data(select_delete_dish_category=category_dish)
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
                                               str_callback_button='deletedishselect')
    await callback.message.answer(text=f'Выберите блюдо котороe вы хотите отредактировать',
                                  reply_markup=keyboard)


# >>>>
@router.callback_query(F.data.startswith('deletedishselectforward'))
async def press_button_select_dish_edit_dish_setting_forward(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'press_button_select_dish_edit_dish_setting_forward: {callback.message.chat.id}')
    user_dict[callback.message.chat.id] = await state.get_data()
    print(user_dict[callback.message.chat.id])
    category_dish = user_dict[callback.message.chat.id]['select_delete_dish_category']
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
                                               str_callback_button='deletedishselect')
    try:
        await callback.message.edit_text(text=f'Выберите блюдо, которое вы хотите отредактировать',
                                         reply_markup=keyboard)
    except:
        await callback.message.edit_text(text=f'Выберите блюдо, котороe вы хотите отредактировать',
                                         reply_markup=keyboard)


# <<<<
@router.callback_query(F.data.startswith('deletedishselectback'))
async def press_button_select_dish_edit_dish_setting_back(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'press_button_select_dish_edit_dish_setting_back: {callback.message.chat.id}')
    user_dict[callback.message.chat.id] = await state.get_data()
    category_dish = user_dict[callback.message.chat.id]['select_delete_dish_category']
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
                                               str_callback_button='deletedishselect')
    try:
        await callback.message.edit_text(text=f'Выберите блюдо, которое вы хотите отредактировать',
                                         reply_markup=keyboard)
    except:
        await callback.message.edit_text(text=f'Выберите блюдо, котороe вы хотите отредактировать',
                                         reply_markup=keyboard)


# МЕНЮ - Редактировать - Категория - Блюда - Выбор атрибута для редактирования
@router.callback_query(F.data.startswith('deletedishselecttextbutton'))
async def press_button_select_dish_delete_setting(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'press_button_select_dish_delete_attribute_setting: {callback.message.chat.id}')
    id_dish = callback.data.split('_')[1]
    await state.update_data(select_delete_dish=id_dish)
    data_id_dish = select_row_id_dish(id_dish)
    print(data_id_dish)
    keyboard = keyboard_delete_select_dish()
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
                                                f"Удалить?",
                                        reply_markup=keyboard)


@router.callback_query(F.data == 'delete_select_dish')
async def press_button_select_dish_confirm_delete(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'press_button_select_dish_confirm_delete: {callback.message.chat.id}')
    await state.set_state(default_state)
    user_dict[callback.message.chat.id] = await state.get_data()
    id_dish = user_dict[callback.message.chat.id]['select_delete_dish']
    dalete_row_table_dish(id_dish)
    keyboard = keyboard_edit_menu()
    await callback.message.answer(text='Выберите пункт',
                                  reply_markup=keyboard)


@router.callback_query(F.data == 'cancel_delete_select_dish')
async def press_button_select_dish_cancel_delete(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'press_button_select_dish_cancel_delete: {callback.message.chat.id}')
    await state.set_state(default_state)
    keyboard = keyboard_edit_menu()
    await callback.message.answer(text='Выберите пункт',
                                  reply_markup=keyboard)
