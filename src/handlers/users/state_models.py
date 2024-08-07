from aiogram.dispatcher.filters.state import StatesGroup, State

class AddDesigner(StatesGroup):
    id = State()
    name = State()
