import asyncio
import logging
import sys

from aiogram import types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
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
    user = await check_user(message.from_user.id)
    users = await get_users()

    if user:
        if message.from_user.id in users['data']['designers']:
            await bot.send_message(message.from_user.id, 'Выберите действие',
                                   reply_markup=await main_keyboard_for_designers())

        elif message.from_user.id in users['data']['main_admins']:
            await bot.send_message(message.from_user.id, 'Выберите действие',
                                   reply_markup=await main_keyboard_for_main_admins())

        else:
            await bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=await main_keyboard_for_admins())
    else:
        await bot.send_message(message.from_user.id,
                               f'Вас нет в базе! Попросите себя добавить! \n{message.from_user.id}')


@dp.message(F.text == 'Отмена')
async def cancel_state(message: types.Message, state: FSMContext):
    await state.clear()
    users = await get_users()

    if users['status'] != 'success':
        await bot.send_message(message.chat.id, 'Произошла ошибка')

    else:
        if message.from_user.id in users['data']['designers']:
            await bot.send_message(message.chat.id, 'Отменено', reply_markup=await main_keyboard_for_designers())

        if message.from_user.id in users['data']['main_admins']:
            await bot.send_message(message.chat.id, 'Отменено', reply_markup=await main_keyboard_for_main_admins())

        else:
            await bot.send_message(message.chat.id, 'Отменено', reply_markup=types.ReplyKeyboardRemove())


async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
