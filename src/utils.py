import requests

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
    return data


def add_work_fc(desinger_id: int, customer: str, headline: str, value: int) -> str:
    json = {
        "customer": customer,
        "headline": headline,
        "value": value,
        "designer_id": desinger_id
    }

    res = requests.post(f'{HOST}/works/add_work', json=json)
    data = res.json()
    return data


def add_designer_fc(id: int, name: str, admin_id: int) -> str:
    params = {
        "admin_id": admin_id
    }
    json = {
        "id": id,
        "name": name,
        "payment": ''
    }

    res = requests.post(f'{HOST}/users/add_designer', json=json, params=params)
    data = res.json()
    return data


if __name__ == '__main__':
    print(add_designer_fc(11234123, 'test', 1284799474))
