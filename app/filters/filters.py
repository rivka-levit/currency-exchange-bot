import logging
import re

from aiogram.filters import BaseFilter
from aiogram.types import Message

logger = logging.getLogger(__name__)


class NumberInMessage(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        pattern = r'^-?\d+\.\d+$'
        text = message.text.strip()

        return text.isdigit() or re.match(pattern, text)
