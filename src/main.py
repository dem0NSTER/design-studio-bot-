import asyncio
import logging
import sys

from aiogram import types, F
from aiogram.filters import CommandStart
from aiogram.methods import DeleteWebhook

from create_bot import bot, dp
from handlers.users.admins import router as router_admins
from handlers.users.designers import router as router_designers
from handlers.works.works import router as router_works
from handlers.other.other import router as router_other
from keyboards import main_keyboard_for_designers, main_keyboard_for_main_admins, main_keyboard_for_admins
from utils import check_user, get_users

dp.include_router(router_admins)
dp.include_router(router_designers)
dp.include_router(router_works)
dp.include_router(router_other)


@dp.message(CommandStart())
async def start(message: types.Message):
    user = check_user(message.from_user.id)
    users = get_users()
    if user:
        if message.from_user.id in users['designers']:
            await bot.send_message(message.from_user.id, 'Выберите действие',
                                   reply_markup=main_keyboard_for_designers())

        elif message.from_user.id in users['main_admins']:
            await bot.send_message(message.from_user.id, 'Выберите действие',
                                   reply_markup=main_keyboard_for_main_admins())

        else:
            await bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=main_keyboard_for_admins())
    else:
        await bot.send_message(message.from_user.id,
                               f'Вас нет в базе! Попросите себя добавить! \n{message.from_user.id}')


async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
