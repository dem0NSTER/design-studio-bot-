from create_bot import bot
from aiogram import types
from utils import get_users


async def check_works(message: types.Message):
    users = get_users()
    if message.from_user.id in users['admins']:
        await bot.send_message(message.chat.id, 'В разработке: 0')
    else:
        await bot.send_message(message.chat.id, 'Вы не админ')


async def create_work(message: types.Message):
    users = get_users()
    if message.from_user.id in users['designers']:
        await bot.send_message(message.chat.id, 'В разработке: 5')
    else:
        await bot.send_message(message.chat.id, 'Вы не дизайнер')


def register_handlers_works(dp):
    dp.register_message_handler(check_works, lambda message: message.text == 'Показать неоплаченные работы')
    dp.register_message_handler(create_work, lambda message: message.text == 'Добавить работу')
