import pytest

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import User, Chat

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


@pytest.fixture(scope='function')
def custom_user():
    """Create a user, can take parameters of user data."""

    payload = {
        'id': 563248,
        'is_bot': False,
        'first_name': 'TestFirstName',
        'last_name': 'TestLastName',
        'username': 'TestUsername',
        'language_code': 'en',
    }

    def _user_factory(**kwargs):
        if kwargs:
            payload.update(kwargs)
        return User(**payload)

    return _user_factory


@pytest.fixture
def user(custom_user) -> User:
    """Sample user with `ru` language code."""

    return custom_user(language_code='ru')


@pytest.fixture
def chat(user) -> Chat:
    """Sample chat with `tg_user` as a user"""

    return Chat(
        id=12,
        type='private',
        title='TestTitle',
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
)
