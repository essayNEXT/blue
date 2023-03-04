# тут має бути імпорт модуля роботи з БД
from aiogram.types import Contact
from typing import Dict
exist_id = []


def user_is_in_database(user_id: int) -> bool:
    """Функція порівнює вказаний user_id з наявними в базі даних.
    У разі наявності такого в БД повератає True"""
    # 386532326
    # exist_id = []  # тут має бути використано запит до БД на витяг всіх зареєстрованих id в базі даних
    global exist_id
    return user_id in exist_id


async def add_guest_to_db(contact: Contact):
    """Функція, що реєструє користувача як 'гостя', з обліковими даними, що вказані в контакті"""
    global exist_id
    exist_id.append(contact.user_id)
    pass


async def update_guest_in_db(user_id: int, user_data: Dict):
    """Функція, що оновлює дані про 'гостя', з обліковими даними, що надаються в словнику"""
    print(user_id)
    print(user_data)
    pass