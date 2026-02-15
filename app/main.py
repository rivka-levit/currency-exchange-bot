import asyncio
import logging

from aiogram import Bot, Dispatcher

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from config import Config, load_config
from database import init_db
from database.create_del_tables import create_tables
from lexicon.lexicon_en import LEXICON_EN
from lexicon.lexicon_ru import LEXICON_RU
from middlewares.i18n import TranslatorMiddleware

from handlers.button_handlers import router as button_router
from handlers.command_handlers import router as commands_router
from handlers.exchange_handlers import router as exchange_router

from interface.main_manu import set_default_main_menu, delete_commands
from interface.bot_description import set_bot_description

logger = logging.getLogger(__name__)

translations = {
    'default': 'en',
    'en': LEXICON_EN,
    'ru': LEXICON_RU,
}


async def on_startup(engine: AsyncEngine):
    await create_tables(engine)


async def main():
    config: Config = load_config()

    logging.basicConfig(
        level=logging.getLevelName(config.log.level),
        format=config.log.format,
        stream=config.log.stream,
    )

    # Start database engine
    db_url = (f'postgresql+asyncpg://{config.db.user}:{config.db.password}'
              f'@{config.db.host}/{config.db.name}')
    engine = create_async_engine(db_url, echo=True)

    bot = Bot(token=config.bot.token, default=config.bot.default)
    dp = Dispatcher()

    dp.startup.register(on_startup)
    dp.startup.register(set_bot_description)
    dp.startup.register(set_default_main_menu)
    dp.shutdown.register(delete_commands)

    # Register middlewares
    dp.update.middleware(TranslatorMiddleware())

    # Register routers
    dp.include_router(commands_router)
    dp.include_router(exchange_router)
    dp.include_router(button_router)

    dp.workflow_data['db'] = init_db()

    await dp.start_polling(
        bot,
        translations=translations,
        engine=engine
    )


if __name__ == '__main__':
    asyncio.run(main())
