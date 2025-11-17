import logging

from aiogram import Bot

logger = logging.getLogger(__name__)


async def set_bot_description(bot: Bot):
    description_text = ("Hi! I'm a currency exchange bot. I can convert the "
                        "amount you entered from one currency into another.")

    success  = await bot.set_my_description(description_text)

    if success:
        logger.info(f'Default description is set')
    else:
        logger.error(f'Failed to set description')
