"""
Bot configuration
"""

import sys

from dataclasses import dataclass
from environs import Env
from io import TextIOWrapper



@dataclass
class TgBot:
    token: str


@dataclass
class LogSettings:
    level: str
    format: str
    stream: TextIOWrapper | None = None


@dataclass
class Config:
    bot: TgBot
    log: LogSettings


def load_config(path: str | None = None) -> Config:
    env = Env()
    if path is None:
        env.read_env()
    else:
        env.read_env(path)

    return Config(
        bot=TgBot(token=env.str("BOT_TOKEN")),
        log=LogSettings(
            level=env.str('LOG_LEVEL'),
            format=env.str('LOG_FORMAT'),
            stream=sys.stdout
        )
    )
