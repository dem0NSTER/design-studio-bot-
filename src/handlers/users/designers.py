from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from create_bot import bot
from handlers.users.state_models import AddDesigner
from keyboards import main_keyboard_for_admins, main_keyboard_for_main_admins, keyboard_to_fsm
from utils import get_users, get_designers, add_designer_fc, check_admin

router = Router()


@router.message(F.text == 'Добавить дизайнера')
async def add_designer(message: types.Message, state: FSMContext):
    is_admin = await check_admin(message.from_user.id)

    if is_admin == 'error':
        await bot.send_message(message.chat.id, 'Произошла ошибка', reply_markup=types.ReplyKeyboardRemove())

    elif is_admin:
        await bot.send_message(message.chat.id, 'Отправте id нового дизайнера. Он должен был его скинуть вам', reply_markup=await keyboard_to_fsm())
        await state.set_state(AddDesigner.id)

    else:
        await bot.send_message(message.chat.id, 'Вы не админ')


@router.message(AddDesigner.id)
async def add_designer_state_id(message: types.Message, state: FSMContext):
    await state.update_data(id=message.text)
    await bot.send_message(message.chat.id, 'Напишите имя дизайнера')
    await state.set_state(AddDesigner.name)


@router.message(AddDesigner.name)
async def add_designer_state_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    await state.clear()
    response = await add_designer_fc(id=data['id'], name=data['name'], admin_id=message.from_user.id)

    users = await get_users()

    if message.from_user.id in users['main_admins']:
        if response['status'] == 'success':
            await bot.send_message(message.chat.id, 'Дизайнер добавлен',
                                   reply_markup=await main_keyboard_for_main_admins())
        else:
            await bot.send_message(message.chat.id, 'Произошла ошибка',
                                   reply_markup=await main_keyboard_for_main_admins())
    else:
        if response['status'] == 'success':
            await bot.send_message(message.chat.id, 'Дизайнер добавлен', reply_markup=await main_keyboard_for_admins())
        else:
            await bot.send_message(message.chat.id, 'Произошла ошибка', reply_markup=await main_keyboard_for_admins())


@router.message(F.text == 'Удалить дизайнера')
async def delete_designer(message: types.Message):
    is_admin = await check_admin(message.from_user.id)
    if is_admin == 'error':
        await bot.send_message(message.chat.id, 'Произошла ошибка')

    elif is_admin:
        response = await get_designers()
        designers = response['data']
        for designer in designers:
            await bot.send_message(message.chat.id, f'{designer["name"]}\n{designer["id"]}')

    else:
        await bot.send_message(message.chat.id, 'Вы не админ')
