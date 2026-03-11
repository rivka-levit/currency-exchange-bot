import pytest

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from tests.mocked_bot import MockedBot


@pytest.fixture(scope='module')
async def storage():
    stg = MemoryStorage()
    try:
        yield stg
    finally:
        await stg.close()


@pytest.fixture(scope='session')
def bot():
    return MockedBot()


@pytest.fixture(scope='session')
async def dispatcher():
    dp = Dispatcher()
    await dp.emit_startup()
    try:
        yield dp
    finally:
        await dp.emit_shutdown()
