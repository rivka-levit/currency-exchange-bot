from aiogram import F, Router
from aiogram.types import CallbackQuery

from sqlalchemy.ext.asyncio import AsyncSession

from callbacks import SourceCurrencyCallbackFactory, TargetCurrencyCallbackFactory

from database.currencies_query import orm_get_available_currencies, orm_get_currency
from database.users_query import orm_get_user, orm_update_user

from keyboards.choice_kb import source_choice_keyboard, target_choice_keyboard
from keyboards.exchange_kb import exchange_keyboard

from lexicon.translator import LocalizedTranslator

router = Router()


@router.callback_query(F.data=='source_choice')
async def source_choice_btn_clicked(
        query: CallbackQuery,
        i18n: LocalizedTranslator,
        session: AsyncSession
):
    currencies = await orm_get_available_currencies(session)
    await query.message.edit_text(
        text=i18n.get('source_choice_msg'),
        reply_markup=source_choice_keyboard(currencies, i18n)
    )


@router.callback_query(F.data=='target_choice')
async def target_choice_btn_clicked(
        query: CallbackQuery,
        i18n: LocalizedTranslator,
        session: AsyncSession
):
    currencies = await orm_get_available_currencies(session)
    await query.message.edit_text(
        text=i18n.get('target_choice_msg'),
        reply_markup=target_choice_keyboard(currencies, i18n)
    )


@router.callback_query(F.data=='reverse')
async def reverse_btn_clicked(
        query: CallbackQuery,
        session: AsyncSession
):
    """Handles reverse button has been clicked."""

    user = await orm_get_user(session, query.from_user.id)
    await orm_update_user(
        session,
        user.tg_id,
        {'source_id': user.target_id, 'target_id': user.source_id}
    )
    await session.refresh(user)
    await query.message.edit_reply_markup(
        reply_markup=exchange_keyboard(source=user.source, target=user.target)
    )


@router.callback_query(SourceCurrencyCallbackFactory.filter())
async def source_currency_btn_chosen(
        query: CallbackQuery,
        callback_data: SourceCurrencyCallbackFactory,
        i18n: LocalizedTranslator,
        session: AsyncSession
):
    """Handles one of source currency buttons has been chosen."""

    user = await orm_get_user(session, query.from_user.id)
    new_source = await orm_get_currency(session, code=callback_data.code)

    await orm_update_user(session, user.tg_id, {'source_id': new_source.id})

    await query.message.edit_text(
        text=i18n.get('set_currencies'),
        reply_markup=exchange_keyboard(source=new_source, target=user.target)
    )


@router.callback_query(TargetCurrencyCallbackFactory.filter())
async def target_currency_btn_chosen(
        query: CallbackQuery,
        callback_data: TargetCurrencyCallbackFactory,
        i18n: LocalizedTranslator,
        session: AsyncSession
):
    """Handles one of target currency buttons has been chosen."""

    user = await orm_get_user(session, query.from_user.id)
    new_target = await orm_get_currency(session, code=callback_data.code)

    await orm_update_user(session, user.tg_id, {'target_id': new_target.id})

    await query.message.edit_text(
        text=i18n.get('set_currencies'),
        reply_markup=exchange_keyboard(source=user.source, target=new_target)
    )


@router.callback_query(F.data=='back_exchange_kb')
async def back_to_exchange_keyboard_btn(
        query: CallbackQuery,
        i18n: LocalizedTranslator,
        session: AsyncSession
):
    """Handles back button to return to set currency screen."""

    user = await orm_get_user(session, query.from_user.id)

    await query.message.edit_text(
        text=i18n.get('set_currencies'),
        reply_markup=exchange_keyboard(source=user.source, target=user.target)
    )
