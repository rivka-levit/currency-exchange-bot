from aiogram import Bot, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from interface.main_manu import set_personal_main_menu

router = Router()


@router.message(CommandStart())
async def handle_start_command(
        message: Message,
        bot: Bot,
        db,
        i18n):
    user_id = message.from_user.id
    if user_id not in db['users']:
        db['users'][user_id] = {'source': 'USD', 'target': 'ILS'}

    await set_personal_main_menu(bot=bot, i18n=i18n)
    await message.answer(text=i18n['start_answer'])
