from aiogram import Bot, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from sqlalchemy.ext.asyncio import AsyncSession

from database.users_query import orm_add_user, orm_get_user

from keyboards.exchange_kb import exchange_keyboard
from interface.main_manu import set_personal_main_menu

router = Router()


@router.message(CommandStart())
async def handle_start_command(
        message: Message,
        bot: Bot,
        i18n,
        session: AsyncSession
):
    """Handles starting the bot."""

    user_id = message.from_user.id
    user = await orm_get_user(session, user_id)
    if not user:
        user_data: dict[str, str | int] = {'tg_id': user_id}
        if name := message.from_user.first_name:
            user_data['first_name'] = name
        if surname := message.from_user.last_name:
            user_data['last_name'] = surname
        if lang := message.from_user.language_code:
            user_data['language'] = lang
        if user_id in bot.admin_ids:  # noqa
            user_data['is_admin'] = True

        await orm_add_user(session, user_data)

        # db['users'][user_id] = {'source': 'USD', 'target': 'ILS'}

    await set_personal_main_menu(bot=bot, i18n=i18n)
    await message.answer(text=i18n['start_answer'])


@router.message(Command(commands=['help']))
async def handle_help_command(message: Message, i18n) -> None:
    """Handles help command."""

    await message.answer(text=i18n['help_answer'])


@router.message(Command(commands=['all_currencies']))
async def handle_all_currencies_command(message: Message, db, i18n) -> None:
    """Handles retrieving all the currencies command."""

    currencies = '\n'.join(
        [f'{code} - {name}' for code, name in db['currencies'].items()]
    )

    await message.answer(text = i18n['/all_currencies'] + currencies)


@router.message(Command(commands=['set_currencies']))
async def handle_set_currencies_command(message: Message, db, i18n) -> None:
    """Handles setting the currencies command."""

    user_id = message.from_user.id

    if user_id not in db['users']:
        db['users'][user_id] = {'source': 'USD', 'target': 'ILS'}

    source = db['users'][user_id]['source']
    target = db['users'][user_id]['target']

    await message.answer(
        text=i18n['/set_currencies'],
        reply_markup=exchange_keyboard(source=source, target=target)
    )
