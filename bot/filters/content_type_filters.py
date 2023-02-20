from aiogram.types import ContentType, Message
from aiogram.filters import BaseFilter


class TextFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.content_type == ContentType.TEXT


class AnimationFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.content_type == ContentType.ANIMATION


class StickerFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.content_type == ContentType.STICKER


class PhotoFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.content_type == ContentType.PHOTO
