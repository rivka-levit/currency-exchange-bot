from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

from sqlalchemy.ext.asyncio import AsyncSession

from database.users_query import orm_get_user
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


class TranslatorMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any]
    ) -> Any:

        user: User = data.get('event_from_user')

        if user is None:
            return await handler(event, data)

        user_lang = user.language_code
        translations = data.get('translations')

        i18n = translations.get(user_lang)
        if i18n is None:
            data["i18n"] = translations[translations["default"]]
        else:
            data["i18n"] = i18n

        return await handler(event, data)
