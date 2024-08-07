from aiogram.dispatcher import FSMContext

from create_bot import bot
from aiogram import types

from utils import get_users, add_designer_fc
from handlers.users.state_models import AddDesigner


async def add_designer(message: types.Message):
    users = get_users()
    if message.from_user.id in users['admins']:
        await bot.send_message(message.chat.id, 'Отправте id нового дизайнера. Он должен был его скинуть вам')
        await AddDesigner.id.set()
    else:
        await bot.send_message(message.chat.id, 'Вы не админ')


async def add_designer_state_2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.text
    await bot.send_message(message.chat.id, 'Напишите имя дизайнера')
    await AddDesigner.name.set()


async def add_designer_state_3(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    response = add_designer_fc(data['id'], data['name'], message.from_user.id)
    if response['status'] == 'success':
        await bot.send_message(message.chat.id, 'Дизайнер добавлен')
    else:
        await bot.send_message(message.chat.id, 'Произошла ошибка')
    await state.finish()


async def delete_designer(message: types.Message):
    users = get_users()
    if message.from_user.id in users['admins']:
        await bot.send_message(message.chat.id, 'В разработке: 1')
    else:
        await bot.send_message(message.chat.id, 'Вы не админ')


def register_handlers_designers(dp):
    dp.register_message_handler(add_designer, lambda message: message.text == 'Добавить дизайнера')
    dp.register_message_handler(delete_designer, lambda message: message.text == 'Удалить дизайнера')
    dp.register_message_handler(add_designer_state_2, state=AddDesigner.id)
    dp.register_message_handler(add_designer_state_3, state=AddDesigner.name)
