from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Currency
from utils.currencies import CURRENCIES


async def orm_create_currencies(session: AsyncSession):
    query = select(Currency)
    result = await session.execute(query)
    if result.first():
        return
    session.add_all(
        [Currency(code=code, name=name) for code, name in CURRENCIES.items()]
    )
    await session.commit()


async def orm_get_currency(
        session: AsyncSession,
        code: str | None = None,
        cur_id: int | None = None
) -> Currency:
    if code:
        query = select(Currency).where(Currency.code == code)
    elif cur_id:
        query = select(Currency).where(Currency.id == cur_id)
    else:
        query = select(Currency).where(Currency.code == '111')
    result = await session.execute(query)
    return result.scalars().one_or_none()


async def orm_get_available_currencies(session: AsyncSession) -> Sequence[Currency]:
    """Gets all available currencies from the database."""

    query = select(Currency).where(Currency.is_available == True)
    result = await session.execute(query)
    return result.scalars().all()
