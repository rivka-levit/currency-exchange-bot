import logging

from aiogram import Bot
from aiogram.types import (BotCommand,
                           BotCommandScopeAllPrivateChats,
                           BotCommandScopeDefault)

from lexicon.lexicon_en import LEXICON_EN

logger = logging.getLogger(__name__)


async def set_default_main_menu(bot: Bot) -> None:
    """Default menu to set on starting the bot."""

    menu_commands = [
        BotCommand(command='start', description=LEXICON_EN['start']),
        BotCommand(command='help', description=LEXICON_EN['help']),
    ]

    logger.info('Setting default main menu...')

    await bot.set_my_commands(
        commands=menu_commands,
        scope=BotCommandScopeDefault()
    )


async def set_personal_main_menu(bot: Bot, i18n: dict[str, str | dict]) -> None:
    """Personal menu to set on /start command."""

    menu_commands = list()

    for command, descr in i18n['commands'].items():
        menu_commands.append(BotCommand(command=command, description=descr))

    logger.info('Setting personal main menu commands...')

    await bot.set_my_commands(
        commands=menu_commands,
        scope=BotCommandScopeAllPrivateChats()
    )


async def delete_commands(bot: Bot) -> None:
    """Delete all commands."""

    logger.info('Deleting all commands...')

    await bot.delete_my_commands(scope=BotCommandScopeAllPrivateChats())
    await bot.delete_my_commands(scope=BotCommandScopeDefault())
