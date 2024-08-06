from aiogram import types
from aiogram.utils import executor
from utils import check_user, get_users
from keyboards import main_keyboard_for_designers, main_keyboard_for_main_admins, main_keyboard_for_admins

from create_bot import bot, dp

from handlers.users.designers import register_handlers_designers
from handlers.users.admins import register_handlers_admins
from handlers.works.works import register_handlers_works
from handlers.other.other import register_handlers_other

register_handlers_designers(dp)
register_handlers_admins(dp)
register_handlers_works(dp)
register_handlers_other(dp)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user = check_user(message.from_user.id)
    users = get_users()
    if user:
        if message.from_user.id in users['designers']:
            await bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=main_keyboard_for_designers())

        elif message.from_user.id in users['main_admins']:
            await bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=main_keyboard_for_main_admins())

        else:
            await bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=main_keyboard_for_admins())
    else:
        await bot.send_message(message.from_user.id, f'Вас нет в базе! Попросите себя добавить! \n{message.from_user.id}')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
