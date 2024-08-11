from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext

from create_bot import bot
from handlers.works.state_models import AddWork
from utils import get_users, add_work_fc
from keyboards import main_keyboard_for_designers

router = Router()

@router.message(F.text == 'Показать неоплаченные работы')
async def check_works(message: types.Message):
    users = get_users()
    if message.from_user.id in users['admins']:
        await bot.send_message(message.chat.id, 'В разработке: 0')
    else:
        await bot.send_message(message.chat.id, 'Вы не админ')


@router.message(F.text == 'Добавить работу')
async def create_work(message: types.Message, state: FSMContext):
    users = get_users()
    if message.from_user.id in users['designers']:
        await bot.send_message(message.chat.id, 'Напишите заказчика (канал)', reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(AddWork.customer)
    else:
        await bot.send_message(message.chat.id, 'Вы не дизайнер')


@router.message(AddWork.customer)
async def create_work_state_customer(message: types.Message, state: FSMContext):
    await state.update_data(customer=message.text)
    await bot.send_message(message.chat.id, 'Напишите название работы')
    await state.set_state(AddWork.headline)


@router.message(AddWork.headline)
async def create_work_state_headline(message: types.Message, state: FSMContext):
    await state.update_data(headline=message.text)
    await bot.send_message(message.chat.id, 'Напишите стоимость работы')
    await state.set_state(AddWork.value)


@router.message(AddWork.value)
async def create_work_state_value(message: types.Message, state: FSMContext):
    await state.update_data(value=message.text)
    data = await state.get_data()
    await state.clear()

    response = add_work_fc(
        desinger_id=message.from_user.id,
        customer=data['customer'],
        headline=data['headline'],
        value=data['value']
    )

    if response['status'] == 'success':
        await bot.send_message(message.chat.id, 'Работа добавлена', reply_markup=main_keyboard_for_designers())
    else:
        await bot.send_message(message.chat.id, 'Произошла ошибка', reply_markup=main_keyboard_for_designers())
