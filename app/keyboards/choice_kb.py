from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callbacks import SourceCurrencyCallbackFactory, TargetCurrencyCallbackFactory


def source_choice_keyboard(currencies: dict[str, str]) -> InlineKeyboardMarkup:
    """Keyboard to choose a source currency."""

    code_buttons = list()

    for code, name in currencies.items():
        currency_btn = InlineKeyboardButton(
            text=code,
            callback_data=SourceCurrencyCallbackFactory(code=code, name=name).pack()
        )
        code_buttons.append(currency_btn)

    builder = InlineKeyboardBuilder()
    builder.row(*code_buttons, width=5)

    return builder.as_markup()


def target_choice_keyboard(currencies: dict[str, str]) -> InlineKeyboardMarkup:
    """Keyboard to choose a target currency."""

    code_buttons = list()

    for code, name in currencies.items():
        currency_btn = InlineKeyboardButton(
            text=code,
            callback_data=TargetCurrencyCallbackFactory(code=code, name=name).pack()
        )
        code_buttons.append(currency_btn)

    builder = InlineKeyboardBuilder()
    builder.row(*code_buttons, width=5)

    return builder.as_markup()
