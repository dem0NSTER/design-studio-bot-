from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext

from create_bot import bot
from handlers.other.state_models import ChangePayment
from keyboards import main_keyboard_for_designers, keyboard_to_fsm
from utils import change_payment_fc, check_designer

router = Router()


@router.message(F.text == 'Изменить способ оплаты')
async def change_payment(message: types.Message, state: FSMContext):
    is_designer = await check_designer(message.from_user.id)

    if is_designer == 'error':
        await bot.send_message(message.chat.id, 'Произошла ошибка', reply_markup=await main_keyboard_for_designers())

    elif is_designer:
        await bot.send_message(message.chat.id, 'отправьте новый способ оплаты', reply_markup=await keyboard_to_fsm())
        await state.set_state(ChangePayment.payment)

    else:
        await bot.send_message(message.chat.id, 'Вы не дизайнер')


@router.message(ChangePayment.payment)
async def change_payment_state_payment(message: types.Message, state: FSMContext):
    await state.update_data(payment=message.text)
    data = await state.get_data()
    await state.clear()

    response = await change_payment_fc(message.from_user.id, data['payment'])

    if response['status'] == 'success':
        await bot.send_message(message.chat.id, 'Способ оплаты изменен', reply_markup=await main_keyboard_for_designers())
    else:
        await bot.send_message(message.chat.id, 'Произошла ошибка', reply_markup=await main_keyboard_for_designers())
