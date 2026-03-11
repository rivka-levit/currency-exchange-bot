import logging

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat

from lexicon.translator import LocalizedTranslator

logger = logging.getLogger(__name__)

COMMAND_NAMES = [
    'start',
    'help',
    'set_currencies',
    'all_currencies'
]


async def set_personal_main_menu(bot: Bot, chat_id: int, i18n: LocalizedTranslator) -> None:
    """Personal menu to set on /start command."""

    menu_commands = list()

    for command in COMMAND_NAMES:
        menu_commands.append(BotCommand(
            command=command,
            description=i18n.get(f'{command}_descr')
        ))

    logger.info('Setting personal main menu commands...')

    await bot.set_my_commands(
        commands=menu_commands,
        scope=BotCommandScopeChat(chat_id=chat_id)
    )


# async def delete_commands(bot: Bot) -> None:
#     """Delete all commands."""
#
#     logger.info('Deleting all commands...')
#
#     await bot.delete_my_commands(scope=BotCommandScopeAllPrivateChats())
