from aiogram.dispatcher.filters.state import State, StatesGroup

class AddWork(StatesGroup):
    customer = State()
    headline = State()
    value = State()
