"""
Handlers to process the amount sent to convert.
"""

from aiogram import Router
from aiogram.types import Message

from exceptions import ConversionRequestError
from filters import NumberInMessage
from lexicon.exchange_message import get_exchange_message
from services.converter import CurrencyConverter

router = Router()


@router.message(NumberInMessage())
async def process_amount_sent(message: Message, db):
    user_id = message.from_user.id
    converter = CurrencyConverter()
    source = db['users'][user_id]['source']
    target = db['users'][user_id]['target']
    amount = float(message.text)

    try:
        result = converter.convert(source, target, amount)
    except ConversionRequestError:
        pass
    else:
        await message.answer(
            text=get_exchange_message(amount, result, user_id, db)
        )
