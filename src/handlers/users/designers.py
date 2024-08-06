from create_bot import bot
from aiogram import types

from utils import get_users


async def add_designer(message: types.Message):
    users = get_users()
    if message.from_user.id in users['admins']:
        await bot.send_message(message.chat.id, 'В разработке: 2')
    else:
        await bot.send_message(message.chat.id, 'Вы не админ')


async def delete_designer(message: types.Message):
    users = get_users()
    if message.from_user.id in users['admins']:
        await bot.send_message(message.chat.id, 'В разработке: 1')
    else:
        await bot.send_message(message.chat.id, 'Вы не админ')


def register_handlers_designers(dp):
    dp.register_message_handler(add_designer, lambda message: message.text == 'Добавить дизайнера')
    dp.register_message_handler(delete_designer, lambda message: message.text == 'Удалить дизайнера')
