from .tables import Users, Languages, Translate_file


async def get_users():
    return await Users.select().run()


async def get_languages():
    return await Languages.select().run()


async def get_json_object():
    return await Translate_file.select().run()