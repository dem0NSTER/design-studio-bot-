from aiogram import types


def main_keyboard_for_designers() -> types.ReplyKeyboardMarkup:
    btns = [
        'Добавить работу',
        'Изменить способ оплаты',
    ]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(*btns)
    return markup


def main_keyboard_for_main_admins() -> types.ReplyKeyboardMarkup:
    btns = [
                'Показать неоплаченные работы',
            ]
    btns_designers = [
        'Добавить дизайнера',
        'Удалить дизайнера',
    ]
    btns_admins = [
        'Добавить админа',
        'Удалить админа',
    ]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(*btns)
    markup.add(*btns_designers)
    markup.add(*btns_admins)
    return markup


def main_keyboard_for_admins() -> types.ReplyKeyboardMarkup:
    btns = [
        'Показать неоплаченные работы',
    ]
    btns_designers = [
        'Добавить дизайнера',
        'Удалить дизайнера',
    ]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(*btns)
    markup.add(*btns_designers)
    return markup
