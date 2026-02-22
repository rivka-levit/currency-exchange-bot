from typing import Any

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from database.currencies_query import orm_get_currency
from database.models import User


async def orm_get_user(session: AsyncSession, user_id: int) -> User:
    """Get one user from database."""

    query = select(User).where(User.tg_id == user_id).options(
        joinedload(User.source),
        joinedload(User.target)
    )
    result = await session.execute(query)
    return result.scalars().one_or_none()


async def orm_add_user(session: AsyncSession, data: dict[str, Any]) -> None:
    """Add user to database."""

    usd = await orm_get_currency(session, 'USD')
    eur = await orm_get_currency(session, 'EUR')

    new_user = User(
        **data,
        source_id=usd.id,
        target_id=eur.id
    )
    session.add(new_user)
    await session.commit()


async def orm_update_user(
        session: AsyncSession,
        user_id: int,
        data: dict[str, Any]
) -> None:
    """Update user data in database."""

    query = update(User).where(User.tg_id == user_id).values(**data)
    await session.execute(query)
    await session.commit()
