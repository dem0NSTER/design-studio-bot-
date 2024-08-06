import requests
from aiogram import types

from config import HOST


def get_users() -> dict:
    res = requests.get(F'{HOST}/users/select_all_users')
    # print(res.text)
    if res.json()['status'] != 'success':
        return 'error'
    return res.json()['data']


def check_user(user_id: int) -> bool or str:
    res = requests.get(F'{HOST}/users/select_all_users')
    # print(res.text)
    data = res.json()
    if data['status'] != 'success':
        return 'error'
    users = data['data']

    admins = users['admins']
    designers = users['designers']
    users_ids = admins + designers
    return user_id in users_ids


def check_admin(admin_id: int) -> bool or str:
    res = requests.get(F'{HOST}/users/select_all_users')
    data = res.json()
    if data['status'] != 'success':
        return 'error'
    users = data['data']

    admins = users['admins']
    return admin_id in admins


def check_main_admin(main_admin_id: int) -> bool or str:
    res = requests.get(F'{HOST}/users/select_main_admins')
    data = res.json()
    if data['status'] != 'success':
        return 'error'
    admins = data['data']
    return main_admin_id in admins


def change_payment_fc(designer_id: int, new_payment: str) -> str:
    params = {
        'designer_id': designer_id,
        'new_payment': new_payment
    }

    res = requests.post(F'{HOST}/users/change_payment', params=params)
    data = res.json()
    return data['status']


if __name__ == '__main__':
    print(change_payment_fc(12, 'hello'))


