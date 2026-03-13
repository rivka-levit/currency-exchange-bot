import pytest

from datetime import datetime
from unittest.mock import patch, AsyncMock

from aiogram.types import Message

from database.models import User
from lexicon.translator import Translator, LocalizedTranslator
from middlewares.i18n import FluentTranslatorMiddleware

pytestmark = pytest.mark.asyncio


async def next_handler(*args, **kwargs):  # noqa
    pass


@pytest.mark.parametrize('lang', ['en', 'ru'])
async def test_i18n_middleware_returns_correct_object(lang, custom_user, chat):
    """Test i18n middleware returns correct translator for existing user."""

    middleware = FluentTranslatorMiddleware()
    translator = Translator()
    user = custom_user(language_code=lang)
    message = Message(
        message_id=153,
        date=datetime.now(),
        chat=chat,
        from_user=user
    )
    data = {
        'event_from_user': user,
        'session': AsyncMock(),
        'translator': translator
    }
    db_user = User(id=156, tg_id=user.id, language=lang)

    with patch(
            'middlewares.i18n.orm_get_user',
            new_callable=AsyncMock,
            return_value=db_user
    ) as mock:
        await middleware(next_handler, message, data)

        assert 'i18n' in data
        mock.assert_awaited_once_with(data['session'], user.id)

        i18n = data['i18n']
        expected_i18n = translator(lang=lang)
        assert isinstance(i18n, LocalizedTranslator)
        assert i18n.get('start_answer') == expected_i18n.get('start_answer')
