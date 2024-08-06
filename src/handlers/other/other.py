from create_bot import bot
from aiogram import types
from aiogram.dispatcher import FSMContext

from utils import get_users, change_payment_fc
from keyboards import main_keyboard_for_designers
from handlers.other.state_models import ChangePayment


async def change_payment(message: types.Message):
    users = get_users()
    if message.from_user.id in users['designers']:
        await bot.send_message(message.chat.id, 'отправьте новый способ оплаты')
        await ChangePayment.payment.set()
    else:
        await bot.send_message(message.chat.id, 'Вы не дизайнер')


async def change_payment_state_2(message: types.Message, state: FSMContext):
    users = get_users()
    if message.from_user.id in users['designers']:
        async with state.proxy() as data:
            data['payment'] = message.text

        if change_payment_fc(message.from_user.id, data['payment']) == 'success':
            await bot.send_message(message.chat.id, 'Способ оплаты изменен', reply_markup=main_keyboard_for_designers())
        else:
            await bot.send_message(message.chat.id, 'Произошла ошибка', reply_markup=main_keyboard_for_designers())
        await state.finish()
    else:
        await bot.send_message(message.chat.id, 'Вы не дизайнер')


def register_handlers_other(dp):
    dp.register_message_handler(change_payment, lambda message: message.text == 'Изменить способ оплаты')
    dp.register_message_handler(change_payment_state_2, state=ChangePayment.payment)
