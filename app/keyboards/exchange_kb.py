from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def exchange_keyboard(source: str, target: str) -> InlineKeyboardMarkup:
    change_btn = InlineKeyboardButton(
        text='🔄',
        callback_data='reverse'
    )
    source_btn = InlineKeyboardButton(
        text=source,
        callback_data='source_choice'
    )
    target_btn = InlineKeyboardButton(
        text=target,
        callback_data='target_choice'
    )

    builder = InlineKeyboardBuilder()
    builder.row(source_btn, change_btn, target_btn, width=3)

    return builder.as_markup()
