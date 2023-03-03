# тут має бути імпорт модуля роботи з БД

exist_id = []


def user_is_in_database(user_id: int) -> bool:
    """Функція порівнює вказаний user_id з наявними в базі даних.
    У разі наявності такого в БД повератає True"""
    # 386532326
    # exist_id = []  # тут має бути використано запит до БД на витяг всіх зареєстрованих id в базі даних
    global exist_id
    return user_id in exist_id


async def add_guest_to_db(user_id: int):
    global exist_id
    exist_id.append(user_id)
