from aiogram.dispatcher.filters.state import StatesGroup, State

class ChangePayment(StatesGroup):
    payment = State()
