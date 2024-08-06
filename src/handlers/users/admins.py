from create_bot import bot
from aiogram import types

from utils import get_users


async def add_admin(message: types.Message):
    users = get_users()
    if message.from_user.id in users['main_admins']:
        await bot.send_message(message.chat.id, 'В разработке: 4')
    else:
        await bot.send_message(message.chat.id, 'Вы не главный админ')


async def delete_admin(message: types.Message):
    users = get_users()
    if message.from_user.id in users['main_admins']:
        await bot.send_message(message.chat.id, 'В разработке: 3')
    else:
        await bot.send_message(message.chat.id, 'Вы не главный админ')


def register_handlers_admins(dp):
    dp.register_message_handler(add_admin, lambda message: message.text == 'Добавить админа')
    dp.register_message_handler(delete_admin, lambda message: message.text == 'Удалить админа')
