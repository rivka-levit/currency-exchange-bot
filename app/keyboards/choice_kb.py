from collections.abc import Sequence

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callbacks import SourceCurrencyCallbackFactory, TargetCurrencyCallbackFactory

from database.models import Currency
from lexicon.translator import LocalizedTranslator


def source_choice_keyboard(
        currencies: Sequence[Currency],
        i18n: LocalizedTranslator
) -> InlineKeyboardMarkup:
    """Keyboard to choose a source currency."""

    code_buttons = list()

    for cur in currencies:
        currency_btn = InlineKeyboardButton(
            text=cur.code,
            callback_data=SourceCurrencyCallbackFactory(
                code=cur.code,
                name=cur.name
            ).pack()
        )
        code_buttons.append(currency_btn)

    back_btn = InlineKeyboardButton(
        text=i18n.get('back_btn'),
        callback_data='back_exchange_kb'
    )

    builder = InlineKeyboardBuilder()
    builder.row(*code_buttons, width=5)
    builder.row(back_btn, width=1)

    return builder.as_markup()


def target_choice_keyboard(
        currencies: Sequence[Currency],
        i18n: LocalizedTranslator
) -> InlineKeyboardMarkup:
    """Keyboard to choose a target currency."""

    code_buttons = list()

    for cur in currencies:
        currency_btn = InlineKeyboardButton(
            text=cur.code,
            callback_data=TargetCurrencyCallbackFactory(
                code=cur.code,
                name=cur.name
            ).pack()
        )
        code_buttons.append(currency_btn)

    back_btn = InlineKeyboardButton(
        text=i18n.get('back_btn'),
        callback_data='back_exchange_kb'
    )

    builder = InlineKeyboardBuilder()
    builder.row(*code_buttons, width=5)
    builder.row(back_btn, width=1)

    return builder.as_markup()
