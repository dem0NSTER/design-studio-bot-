from aiogram.fsm.state import StatesGroup, State


class AddDesigner(StatesGroup):
    id = State()
    name = State()


class AddAdmin(StatesGroup):
    id = State()
    name = State()
