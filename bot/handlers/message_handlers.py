from aiogram import Router, types
from aiogram.types import Message
from blue.bot.filters.content_type_filters import TextFilter, PhotoFilter, StickerFilter, AnimationFilter

router = Router()


@router.message(TextFilter())
async def message_with_text(message: types.Message):
    await message.answer("Це текстове повідомлення!")


@router.message(StickerFilter())
async def message_with_sticker(message: Message):
    await message.answer("Це стікер!")


@router.message(AnimationFilter())
async def message_with_gif(message: Message):
    await message.answer("Це GIF!")


@router.message(PhotoFilter())
async def message_with_gif(message: Message):
    await message.answer("Це фото!")




