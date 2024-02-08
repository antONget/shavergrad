from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter

from config_data.config import Config, load_config
from module.database import create_table_dish, create_table_promotion, insert_data_table_dish, \
    insert_data_table_promotion, select_all_data_table_promotion, delete_row_table_promotion, select_row_table_promotion, \
    delete_all_promotion
from keyboards.keyboards_admin import keyboard_dish_in_stop, keyboard_confirmation_add_dish, keyboard_edit_menu,\
    keyboard_continue_add_dish, keyboards_superadmin, keyboard_pass_add_photo_promotion, keyboard_confirm_add_promotion, \
    keyboard_edit_promotion, keyboards_select_dish_edit_menu, keyboard_confirm_del_promotion, keyboard_confirm_del_all_promotion
import logging

router = Router()
config: Config = load_config()


class Promotion(StatesGroup):
    photo_promo = State()
    description_promo = State()
    short_promo = State()


user_dict = {}


@router.callback_query(F.data == 'add_promotion')
async def press_button_add_promotion(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'press_button_add_promotion: {callback.message.chat.id}')
    await callback.message.answer(text=f'Пришлите изображение для акции или скидки',
                                  reply_markup=keyboard_pass_add_photo_promotion())
    await state.set_state(Promotion.photo_promo)


@router.message(F.photo, StateFilter(Promotion.photo_promo))
async def get_picture_promotion(message: Message, state: FSMContext) -> None:
    logging.info(f'get_picture_promotion: {message.chat.id}')
    id_photo = message.photo[-1].file_id
    await state.update_data(promotion_picture=id_photo)
    await message.answer(text=f'Пришлите описание акции')
    await state.set_state(Promotion.description_promo)


@router.message(StateFilter(Promotion.photo_promo))
async def get_picture_promotion(message: Message) -> None:
    logging.info(f'get_picture_promotion: {message.chat.id}')
    await message.answer(text=f'Это не похоже на фото!')


@router.callback_query(F.data == 'pass_add_photo_promotion', StateFilter(Promotion.photo_promo))
async def press_pass_add_photo_promotion(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'press_pass_add_photo_promotion: {callback.message.chat.id}')
    await state.update_data(promotion_picture='none')
    await callback.message.answer(text=f'Пришлите описание акции')
    await state.set_state(Promotion.description_promo)


@router.message(F.text, StateFilter(Promotion.description_promo))
async def get_description_promotion(message: Message, state: FSMContext) -> None:
    logging.info(f'get_description_dish: {message.chat.id}')
    await state.update_data(promotion_description=message.text)
    await message.answer(text=f'Пришлите короткое описание (идентификатор) акции, которое будет отображаться'
                              f' администратору при редактирование раздела "Акции и скидки"')
    await state.set_state(Promotion.short_promo)


@router.message(F.text, StateFilter(Promotion.short_promo))
async def get_short_promotion(message: Message, state: FSMContext) -> None:
    logging.info(f'get_short_promotion: {message.chat.id}')
    await state.update_data(promotion_short=message.text)
    user_dict[message.chat.id] = await state.get_data()
    if user_dict[message.chat.id]['promotion_picture'] != 'none':
        await message.answer_photo(photo=user_dict[message.chat.id]['promotion_picture'],
                                   caption=user_dict[message.chat.id]['promotion_description'],
                                   reply_markup=keyboard_confirm_add_promotion())
    else:
        await message.answer(text=user_dict[message.chat.id]['promotion_description'],
                             reply_markup=keyboard_confirm_add_promotion())
    await state.set_state(default_state)


@router.callback_query(F.data == 'confirm_add_promotion')
async def press_confirm_add_promotion(callback: CallbackQuery) -> None:
    logging.info(f'press_confirm_add_promotion: {callback.message.chat.id}')
    insert_data_table_promotion(description=user_dict[callback.message.chat.id]['promotion_description'],
                                image=user_dict[callback.message.chat.id]['promotion_picture'],
                                short_description=user_dict[callback.message.chat.id]['promotion_short'])
    keyboard = keyboard_edit_promotion()
    await callback.message.answer(text='Редактирование раздела "Скидки и акции"',
                                  reply_markup=keyboard)


@router.callback_query(F.data == 'cancel_add_promotion')
async def press_cancel_add_promotion(callback: CallbackQuery) -> None:
    logging.info(f'press_cancel_add_promotion: {callback.message.chat.id}')
    keyboard = keyboard_edit_promotion()
    await callback.message.answer(text='Редактирование раздела "Скидки и акции"',
                                  reply_markup=keyboard)


@router.callback_query(F.data == 'delete_promotion')
async def press_delete_promotion(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'press_delete_promotion: {callback.message.chat.id}')
    data_all_promotion = select_all_data_table_promotion()
    list_data_button = [row[3] for row in data_all_promotion]
    list_id_callback = [row[0] for row in data_all_promotion]
    back = 0
    forward = 2
    count_item = 6
    keyboard = keyboards_select_dish_edit_menu(list_data_button=list_data_button,
                                               list_id_callback=list_id_callback,
                                               back=back,
                                               forward=forward,
                                               count=count_item,
                                               str_callback_button='delpromotion')
    await callback.message.answer(text=f'Выберите что вы хотите удалить',
                                  reply_markup=keyboard)


# >>>>
@router.callback_query(F.data.startswith('delpromotionforward'))
async def press_delete_promotion_forward(callback: CallbackQuery) -> None:
    logging.info(f'press_delete_promotion_forward: {callback.message.chat.id}')
    data_all_promotion = select_all_data_table_promotion()
    list_data_button = [row[3] for row in data_all_promotion]
    list_id_callback = [row[0] for row in data_all_promotion]
    forward = int(callback.data.split('_')[1]) + 1
    back = forward - 2
    count_item = 6
    keyboard = keyboards_select_dish_edit_menu(list_data_button=list_data_button,
                                               list_id_callback=list_id_callback,
                                               back=back,
                                               forward=forward,
                                               count=count_item,
                                               str_callback_button='delpromotion')
    try:
        await callback.message.edit_text(text=f'Выберите что вы хотите удалить',
                                         reply_markup=keyboard)
    except:
        await callback.message.edit_text(text=f'Выберите что вы хотитe удалить',
                                         reply_markup=keyboard)


# <<<<
@router.callback_query(F.data.startswith('delpromotionback'))
async def press_delete_promotion_back(callback: CallbackQuery) -> None:
    logging.info(f'ppress_delete_promotion_back: {callback.message.chat.id}')
    data_all_promotion = select_all_data_table_promotion()
    list_data_button = [row[3] for row in data_all_promotion]
    list_id_callback = [row[0] for row in data_all_promotion]
    back = int(callback.data.split('_')[1]) - 1
    forward = back + 2
    count_item = 6
    keyboard = keyboards_select_dish_edit_menu(list_data_button=list_data_button,
                                               list_id_callback=list_id_callback,
                                               back=back,
                                               forward=forward,
                                               count=count_item,
                                               str_callback_button='delpromotion')
    try:
        await callback.message.edit_text(text=f'Выберите что вы хотите удалить',
                                         reply_markup=keyboard)
    except:
        await callback.message.edit_text(text=f'Выберите что вы хотитe удалить',
                                         reply_markup=keyboard)


@router.callback_query(F.data.startswith('delpromotiontextbutton'))
async def press_button_select_delete(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'press_button_select_dish_edit_dish_setting: {callback.message.chat.id}')
    id_promotion = int(callback.data.split('_')[1])
    print(id_promotion)
    await state.update_data(id_promotion_delete=id_promotion)
    row_promotion = select_row_table_promotion(id_promotion)
    print(row_promotion)
    await callback.message.answer(text=f'Вы действительно хотите удалить акцию {row_promotion[3]}',
                                  reply_markup=keyboard_confirm_del_promotion())


@router.callback_query(F.data == 'confirm_del_promotion')
async def press_button_confirm_del_promotion(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'press_button_confirm_del_promotion: {callback.message.chat.id}')
    user_dict[callback.message.chat.id] = await state.get_data()
    delete_row_table_promotion(user_dict[callback.message.chat.id]['id_promotion_delete'])
    await callback.message.answer(text=f'Акция успешно удалена')
    keyboard = keyboard_edit_promotion()
    await callback.message.answer(text='Редактирование раздела "Скидки и акции"',
                                  reply_markup=keyboard)


@router.callback_query(F.data == 'cancel_del_promotion')
async def press_button_cancel_del_promotion(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'press_button_cancel_del_promotion: {callback.message.chat.id}')
    keyboard = keyboard_edit_promotion()
    await callback.message.answer(text='Редактирование раздела "Скидки и акции"',
                                  reply_markup=keyboard)


@router.callback_query(F.data == 'delete_all_promotion')
async def press_button_delete_all_promotion(callback: CallbackQuery) -> None:
    logging.info(f'press_button_delete_all_promotion: {callback.message.chat.id}')
    keyboard = keyboard_confirm_del_all_promotion()
    await callback.message.answer(text='Вы действительно желаете удалить все акции?',
                                  reply_markup=keyboard)


@router.callback_query(F.data == 'cancel_del_all_promotion')
async def press_button_cancel_del_all_promotion(callback: CallbackQuery) -> None:
    logging.info(f'press_button_cancel_del_all_promotion: {callback.message.chat.id}')
    keyboard = keyboard_edit_promotion()
    await callback.message.answer(text='Редактирование раздела "Скидки и акции"',
                                  reply_markup=keyboard)


@router.callback_query(F.data == 'confirm_del_all_promotion')
async def press_button_confirm_del_all_promotion(callback: CallbackQuery) -> None:
    logging.info(f'press_button_confirm_del_all_promotion: {callback.message.chat.id}')
    delete_all_promotion()
    await callback.message.answer(text=f'Все акции удалены')
    keyboard = keyboard_edit_promotion()
    await callback.message.answer(text='Редактирование раздела "Скидки и акции"',
                                  reply_markup=keyboard)

