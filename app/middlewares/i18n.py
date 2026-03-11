from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

from sqlalchemy.ext.asyncio import AsyncSession

from database.query_users import orm_get_user
from lexicon.translator import Translator


class FluentTranslatorMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any]
    ) -> Any:
        translator = Translator()
        tg_user: User = data.get('event_from_user')

        if tg_user:
            session: AsyncSession = data.get('session')
            user = await orm_get_user(session, tg_user.id)
            if user:
                data['i18n'] = translator(lang=user.language)
            else:
                data['i18n'] = translator(lang=tg_user.language_code)
        else:
            data['i18n'] = translator(lang='en')

        return await handler(event, data)
