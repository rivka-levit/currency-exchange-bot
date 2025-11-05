import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import Config, load_config
from lexicon.lexicon_en import LEXICON_EN
from lexicon.lexicon_ru import LEXICON_RU


logger = logging.getLogger(__name__)

translations = {
    'default': 'en',
    'en': LEXICON_EN,
    'ru': LEXICON_RU,
}


async def main():
    config: Config = load_config()

    logging.basicConfig(
        level=logging.getLevelName(config.log.level),
        format=config.log.format,
        stream=config.log.stream,
    )

    bot = Bot(token=config.bot.token)
    dp = Dispatcher()

    # Register routers

    # Register middlewares

    await dp.start_polling(bot=bot, translations=translations)


if __name__ == '__main__':
    asyncio.run(main())
