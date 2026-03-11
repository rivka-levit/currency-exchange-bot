"""
Handlers to process the amount sent to convert.
"""

from aiogram import Router
from aiogram.types import Message

from sqlalchemy.ext.asyncio import AsyncSession

from database.users_query import orm_get_user

from exceptions import ConversionRequestError
from filters import NumberInMessage
from lexicon.translator import LocalizedTranslator
from services.converter import CurrencyConverter
from utils.exchange_message import get_exchange_message

router = Router()


@router.message(NumberInMessage())
async def process_amount_sent(message: Message, session: AsyncSession):
    """Handles amount sent to convert."""

    user = await orm_get_user(session, message.from_user.id)
    converter = CurrencyConverter()

    source = user.source.code
    target = user.target.code
    amount = float(message.text.strip())

    try:
        result = converter.convert(source, target, amount)
    except ConversionRequestError:
        pass
    else:
        await message.answer(
            text=get_exchange_message(amount, result, source, target)
        )


@router.message()
async def process_other_messages(message: Message, i18n: LocalizedTranslator):
    """Handles other messages sent to bot."""

    await message.answer(text=i18n.get('wrong_msg'))
