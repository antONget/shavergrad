from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter

from config_data.config import Config, load_config
from module.database import create_table_dish, create_table_promotion, insert_data_table_dish
from keyboards.keyboards_admin import keyboard_dish_in_stop, keyboard_confirmation_add_dish, keyboard_edit_menu,\
    keyboard_continue_add_dish, keyboards_superadmin
import logging

router = Router()
config: Config = load_config()


class Dish_add(StatesGroup):
    add_name_dish = State()
    add_description_dish = State()
    add_photo_dish = State()
    add_cost_dish = State()
    add_category_dish = State()

user_dict = {}


@router.callback_query(F.data == 'add_dish')
async def press_button_add_dish_setting(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'press_button_add_dish_setting: {callback.message.chat.id}')
    await callback.message.answer(text=f'Пришлите наименования блюда')
    await state.set_state(Dish_add.add_name_dish)


@router.message(F.text, StateFilter(Dish_add.add_name_dish))
async def get_name_dish(message: Message, state: FSMContext) -> None:
    logging.info(f'get_name_dish: {message.chat.id}')
    await state.update_data(add_name_dish=message.text)
    await message.answer(text=f'Пришлите описание блюда')
    await state.set_state(Dish_add.add_description_dish)


@router.message(F.text, StateFilter(Dish_add.add_description_dish))
async def get_description_dish(message: Message, state: FSMContext) -> None:
    logging.info(f'get_description_dish: {message.chat.id}')
    await state.update_data(add_description_dish=message.text)
    await message.answer(text=f'Пришлите фото блюда')
    await state.set_state(Dish_add.add_photo_dish)


@router.message(F.photo, StateFilter(Dish_add.add_photo_dish))
async def get_picture_dish(message: Message, state: FSMContext) -> None:
    logging.info(f'get_picture_dish: {message.chat.id}')
    id_photo = message.photo[-1].file_id
    await state.update_data(add_picture_dish=id_photo)
    await message.answer(text=f'Пришлите стоимость блюда')
    await state.set_state(Dish_add.add_cost_dish)


@router.message(F.text, StateFilter(Dish_add.add_cost_dish), lambda x: x.text.isdigit() and int(x.text) > 0)
async def get_cost_dish(message: Message, state: FSMContext) -> None:
    logging.info(f'get_cost_dish: {message.chat.id}')
    await state.update_data(add_cost_dish=int(message.text))
    await message.answer(text=f'Пришлите категорию блюда')
    await state.set_state(Dish_add.add_category_dish)


@router.message(F.text, StateFilter(Dish_add.add_cost_dish))
async def get_cost_dish(message: Message, state: FSMContext) -> None:
    logging.info(f'get_cost_dish: {message.chat.id}')
    await message.answer(text=f'Повторите ввод, введено не корректное значение')


@router.message(F.text, StateFilter(Dish_add.add_category_dish))
async def get_category_dish(message: Message, state: FSMContext) -> None:
    logging.info(f'get_category_dish: {message.chat.id}')
    await state.update_data(add_category_dish=message.text)
    await message.answer(text=f'Блюдо уже доступно к заказу?',
                         reply_markup=keyboard_dish_in_stop())
    await state.set_state(default_state)


@router.callback_query(F.data == 'dish_not_in_stop')
async def press_dish_not_in_stop(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'press_button_add_dish_setting: {callback.message.chat.id}')
    await state.update_data(add_in_stop=1)
    await callback.message.answer(text=f'Подтверждение добавления блюда',
                                  reply_markup=keyboard_confirmation_add_dish())


@router.callback_query(F.data == 'dish_in_stop')
async def press_dish_in_stop(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'press_button_add_dish_setting: {callback.message.chat.id}')
    await state.update_data(add_in_stop=0)
    await callback.message.answer(text=f'Подтверждение добавления блюда',
                                  reply_markup=keyboard_confirmation_add_dish())


@router.callback_query(F.data == 'add_dish_done')
async def press_add_dish_done(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'press_add_dish_done: {callback.message.chat.id}')
    user_dict[callback.message.chat.id] = await state.get_data()
    print(user_dict[callback.message.chat.id])
    name_dish = user_dict[callback.message.chat.id]['add_name_dish']
    cost_dish = user_dict[callback.message.chat.id]['add_cost_dish']
    category_dish = user_dict[callback.message.chat.id]['add_category_dish']
    description_dish = user_dict[callback.message.chat.id]['add_description_dish']
    picture_dish = user_dict[callback.message.chat.id]['add_picture_dish']
    is_stop = user_dict[callback.message.chat.id]['add_in_stop']
    insert_data_table_dish(name_dish=name_dish, cost_dish=cost_dish, category_dish=category_dish,
                           description_dish=description_dish, picture_dish=picture_dish, is_stop=is_stop)
    await callback.message.answer(text=f'Блюдо успешно добавлено в базу',
                                  reply_markup=keyboard_continue_add_dish())


@router.callback_query(F.data == 'cancel_add_dish')
async def press_cancel_add_dish(callback: CallbackQuery) -> None:
    logging.info(f'press_cancel_add_dish: {callback.message.chat.id}')
    keyboard = keyboard_edit_menu()
    await callback.message.answer(text='Выберите пункт',
                                  reply_markup=keyboard)


@router.callback_query(F.data == 'continue_add_dish')
async def press_continue_add_dish(callback: CallbackQuery) -> None:
    logging.info(f'press_continue_add_dish: {callback.message.chat.id}')
    keyboard = keyboards_superadmin()
    await callback.message.answer(text='Выберите какой раздел вы хотите отредактировать',
                                  reply_markup=keyboard)


@router.callback_query(F.data == 'finish_add_dish')
async def press_finish_add_dish(callback: CallbackQuery) -> None:
    logging.info(f'press_finish_add_dish: {callback.message.chat.id}')
    keyboard = keyboard_edit_menu()
    await callback.message.answer(text='Выберите пункт',
                                  reply_markup=keyboard)
