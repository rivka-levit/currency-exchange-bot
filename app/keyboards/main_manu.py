import logging

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats

logger = logging.getLogger(__name__)


async def set_main_menu(bot: Bot, i18n: dict[str, str | dict]) -> None:
    menu_commands = list()

    for command, descr in i18n['commands'].items():
        menu_commands.append(BotCommand(command=command, description=descr))

    logger.info('Setting main menu commands...')

    await bot.set_my_commands(
        commands=menu_commands,
        scope=BotCommandScopeAllPrivateChats()
    )
