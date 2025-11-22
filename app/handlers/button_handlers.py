from aiogram import F, Router
from aiogram.types import CallbackQuery

from callbacks import SourceCurrencyCallbackFactory, TargetCurrencyCallbackFactory
from keyboards.choice_kb import source_choice_keyboard, target_choice_keyboard
from keyboards.exchange_kb import exchange_keyboard

router = Router()


@router.callback_query(F.data=='source_choice')
async def source_choice_btn_clicked(query: CallbackQuery, db, i18n):
    await query.message.edit_text(
        text=i18n['source_choice_msg'],
        reply_markup=source_choice_keyboard(db['currencies'])
    )


@router.callback_query(F.data=='target_choice')
async def source_choice_btn_clicked(query: CallbackQuery, db, i18n):
    await query.message.edit_text(
        text=i18n['target_choice_msg'],
        reply_markup=target_choice_keyboard(db['currencies'])
    )


@router.callback_query(F.data=='reverse')
async def reverse_btn_clicked(query: CallbackQuery, db, i18n):
    user_id = query.from_user.id
    new_source = db['users'][user_id]['target']
    new_target = db['users'][user_id]['source']

    db['users'][user_id]['source'] = new_source
    db['users'][user_id]['target'] = new_target

    await query.message.edit_reply_markup(
        reply_markup=exchange_keyboard(source=new_source, target=new_target)
    )

    await query.answer(text=i18n['reverse_msg'], show_alert=True)


@router.callback_query(SourceCurrencyCallbackFactory.filter())
async def source_currency_btn_chosen(
        query: CallbackQuery,
        callback_data: SourceCurrencyCallbackFactory,
        db,
        i18n
):
    """Handles one of source currency buttons has been chosen."""

    user_id = query.from_user.id
    new_source = callback_data.code
    db['users'][user_id]['source'] = new_source

    await query.message.edit_text(
        text=i18n['/set_currencies'],
        reply_markup=exchange_keyboard(
            source=new_source,
            target=db['users'][user_id]['target']
        )
    )
    await query.answer(text=i18n['source_set_msg'], show_alert=True)


@router.callback_query(TargetCurrencyCallbackFactory.filter())
async def target_currency_btn_chosen(
        query: CallbackQuery,
        callback_data: TargetCurrencyCallbackFactory,
        db,
        i18n
):
    """Handles one of target currency buttons has been chosen."""

    user_id = query.from_user.id
    new_target = callback_data.code
    db['users'][user_id]['target'] = new_target

    await query.message.edit_text(
        text=i18n['/set_currencies'],
        reply_markup=exchange_keyboard(
            source=db['users'][user_id]['source'],
            target=new_target
        )
    )
    await query.answer(text=i18n['taget_set_msg'], show_alert=True)
