from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from create_bot import bot
from handlers.users.state_models import AddAdmin
from keyboards import main_keyboard_for_main_admins, keyboard_to_fsm
from utils import get_admins, add_admin_fc

router = Router()


@router.message(F.text == 'Добавить админа')
async def add_admin(message: types.Message, state: FSMContext):
    is_main_admin = await get_admins()

    if is_main_admin == 'error':
        await bot.send_message(message.chat.id, 'Произошла ошибка', reply_markup=await main_keyboard_for_main_admins())

    elif is_main_admin:
        await bot.send_message(message.chat.id, 'Отпрате id нового админа. Он должен был его скинуть вам', reply_markup=await keyboard_to_fsm())
        await state.set_state(AddAdmin.id)

    else:
        await bot.send_message(message.chat.id, 'Вы не главный админ')


@router.message(AddAdmin.id)
async def add_admin_state_id(message: types.Message, state: FSMContext):
    await state.update_data(id=message.text)
    await bot.send_message(message.chat.id, 'Напишите имя админа')
    await state.set_state(AddAdmin.name)


@router.message(AddAdmin.name)
async def add_admin_state_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    await state.clear()

    response = await add_admin_fc(id=data['id'], name=data['name'], id_main_admin=message.from_user.id)

    if response['status'] == 'success':
        await bot.send_message(message.chat.id, 'Админ добавлен', reply_markup=await main_keyboard_for_main_admins())
    else:
        await bot.send_message(message.chat.id, 'Произошла ошибка', reply_markup=await main_keyboard_for_main_admins())


@router.message(F.text == 'Удалить админа')
async def delete_admin(message: types.Message):
    is_main_admin = await get_admins()

    if is_main_admin == 'error':
        await bot.send_message(message.chat.id, 'Произошла ошибка')

    elif is_main_admin:
        response = await get_admins()

        if response['status'] != 'success':
            await bot.send_message(message.chat.id, 'Произошла ошибка')

        else:
            admins = response['data']
            for admin in admins:
                await bot.send_message(message.chat.id, f'{admin["name"]}\n{admin["id"]}')

    else:
        await bot.send_message(message.chat.id, 'Вы не главный админ')
