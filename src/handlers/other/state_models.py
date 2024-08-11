from aiogram.fsm.state import StatesGroup, State


class ChangePayment(StatesGroup):
    payment = State()
