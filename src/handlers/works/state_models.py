from aiogram.fsm.state import StatesGroup, State


class AddWork(StatesGroup):
    customer = State()
    headline = State()
    value = State()
