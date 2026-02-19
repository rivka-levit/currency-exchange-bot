"""
Bot configuration
"""

import sys

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from dataclasses import dataclass
from environs import Env
from io import TextIOWrapper



@dataclass
class TgBot:
    token: str
    admin_ids: set[int]
    default: DefaultBotProperties


@dataclass
class DatabaseConfig:
    name: str
    host: str
    port: int
    user: str
    password: str


@dataclass
class LogSettings:
    level: str
    format: str
    stream: TextIOWrapper | None = None


@dataclass
class Config:
    bot: TgBot
    db: DatabaseConfig
    log: LogSettings


def load_config(path: str | None = None) -> Config:
    env = Env()
    if path is None:
        env.read_env()
    else:
        env.read_env(path)

    return Config(
        bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids={int(i) for i in env.str('ADMIN_IDS').split(',')},
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        ),
        db=DatabaseConfig(
            name=env.str('POSTGRES_DB'),
            host=env.str('POSTGRES_HOST'),
            port=env.int('POSTGRES_PORT'),
            user=env.str('POSTGRES_USER'),
            password=env.str('POSTGRES_PASSWORD'),
        ),
        log=LogSettings(
            level=env.str('LOG_LEVEL'),
            format=env.str('LOG_FORMAT'),
            stream=sys.stdout
        )
    )
