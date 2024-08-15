import aiohttp
import asyncio

from config import HOST


async def async_get_admins() -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{HOST}/users/select_all_admins') as response:
            return await response.json()


async def get_admins() -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(F'{HOST}/users/select_all_admins') as response:
            return await response.json()


async def get_designers() -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(F'{HOST}/users/select_all_designers') as response:
            return await response.json()


async def get_users() -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(F'{HOST}/users/select_all_users') as response:
            return await response.json()


async def check_user(user_id: int) -> bool or str:
    data = await get_users()
    if data['status'] != 'success':
        return 'error'
    users = data['data']

    admins = users['admins']
    designers = users['designers']
    users_ids = admins + designers
    return user_id in users_ids


async def check_admin(admin_id: int) -> bool or str:
    data = await get_users()
    if data['status'] != 'success':
        return 'error'

    admins = data['data']['admins']
    return admin_id in admins


async def check_designer(designer_id: int) -> bool or str:
    data = await get_users()
    if data['status'] != 'success':
        return 'error'

    designers = data['data']['designers']
    return designer_id in designers


async def check_main_admin(main_admin_id: int) -> bool or str:
    data = await get_users()
    if data['status'] != 'success':
        return 'error'

    admins = data['data']['main_admins']
    return main_admin_id in admins


async def change_payment_fc(designer_id: int, new_payment: str) -> str:
    params = {
        'designer_id': designer_id,
        'new_payment': new_payment
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(F'{HOST}/users/change_payment', params=params) as response:
            return await response.json()


async def add_work_fc(desinger_id: int, customer: str, headline: str, value: int) -> str:
    json = {
        "customer": customer,
        "headline": headline,
        "value": value,
        "designer_id": desinger_id
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(F'{HOST}/works/add_work', json=json) as response:
            return await response.json()


async def add_designer_fc(id: int, name: str, admin_id: int) -> str:
    params = {
        "admin_id": admin_id
    }
    json = {
        "id": id,
        "name": name,
        "payment": ''
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(F'{HOST}/users/add_designer', json=json, params=params) as response:
            return await response.json()


async def add_admin_fc(id: int, name: str, id_main_admin: int) -> str:
    params = {
        "id_main_admin": id_main_admin
    }
    json = {
        "id": id,
        "name": name,
        "is_main_admin": False
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(F'{HOST}/users/add_admin', json=json, params=params) as response:
            return await response.json()


if __name__ == '__main__':
   a = asyncio.run(check_main_admin(1))
   print(a)
