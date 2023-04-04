from .tables import Users, Languages


async def get_users():
    return await Users.select().run()


async def get_languages():
    return await Languages.select().run()