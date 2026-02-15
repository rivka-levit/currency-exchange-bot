from sqlalchemy.ext.asyncio import AsyncEngine

from database.models import Base


async def create_tables(engine: AsyncEngine):
    async with engine.begin() as conn:  # noqa
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables(engine: AsyncEngine):
    async with engine.begin() as conn:  # noqa
        await conn.run_sync(Base.metadata.drop_all)
