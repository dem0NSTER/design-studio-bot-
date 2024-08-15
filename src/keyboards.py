from aiogram.utils.keyboard import KeyboardButton, ReplyKeyboardMarkup


async def main_keyboard_for_designers() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Добавить работу'), KeyboardButton(text='Изменить способ оплаты')],
    ], resize_keyboard=True)

    return markup


async def main_keyboard_for_main_admins() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Показать неоплаченные работы')],
        [KeyboardButton(text='Добавить админа'), KeyboardButton(text='Удалить админа')],
        [KeyboardButton(text='Добавить дизайнера'), KeyboardButton(text='Удалить дизайнера')],
    ], resize_keyboard=True)

    return markup


async def main_keyboard_for_admins() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Показать неоплаченные работы')],
        [KeyboardButton(text='Добавить дизайнера'), KeyboardButton(text='Удалить дизайнера')],
    ], resize_keyboard=True)

    return markup


async def keyboard_to_fsm() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Отмена')]
    ], resize_keyboard=True)

    return markup
