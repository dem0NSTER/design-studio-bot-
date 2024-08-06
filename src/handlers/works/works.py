from aiogram import types
from aiogram.dispatcher import FSMContext

from create_bot import bot
from handlers.works.state_models import AddWork
from utils import get_users, add_work_fc
from keyboards import main_keyboard_for_designers


async def check_works(message: types.Message):
    users = get_users()
    if message.from_user.id in users['admins']:
        await bot.send_message(message.chat.id, 'В разработке: 0')
    else:
        await bot.send_message(message.chat.id, 'Вы не админ')


async def create_work(message: types.Message):
    users = get_users()
    if message.from_user.id in users['designers']:
        await bot.send_message(message.chat.id, 'Напишите заказчика (канал)')
        await AddWork.customer.set()
    else:
        await bot.send_message(message.chat.id, 'Вы не дизайнер')


async def create_work_state_2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['customer'] = message.text
    await bot.send_message(message.chat.id, 'Напишите название работы')
    await AddWork.headline.set()


async def create_work_state_3(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['headline'] = message.text
    await bot.send_message(message.chat.id, 'Напишите стоимость работы')
    await AddWork.value.set()


async def create_work_state_4(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['value'] = message.text

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
    await state.finish()


def register_handlers_works(dp):
    dp.register_message_handler(check_works, lambda message: message.text == 'Показать неоплаченные работы')
    dp.register_message_handler(create_work, lambda message: message.text == 'Добавить работу')
    dp.register_message_handler(create_work_state_2, state=AddWork.customer)
    dp.register_message_handler(create_work_state_3, state=AddWork.headline)
    dp.register_message_handler(create_work_state_4, state=AddWork.value)
