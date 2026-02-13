from typing import Set

from sqlalchemy import Boolean, DateTime, ForeignKey, func, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now()
    )


class Currency(Base):
    __tablename__ = 'currency_table'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(3), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)

    source_users: Mapped[Set['User']] = relationship(back_populates='source')
    target_users: Mapped[Set['User']] = relationship(back_populates='target')


class User(Base):
    __tablename__ = 'user_table'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(150), nullable=True)
    last_name: Mapped[str] = mapped_column(String(150), nullable=True)
    phone: Mapped[str] = mapped_column(String(13), nullable=True)
    language: Mapped[str] = mapped_column(String(3), default='en')

    source_id: Mapped[int] = mapped_column(ForeignKey('currency_table.id'), nullable=False)
    target_id: Mapped[int] = mapped_column(ForeignKey('currency_table.id'), nullable=False)
    source: Mapped['Currency'] = relationship(back_populates='source_users')
    target: Mapped['Currency'] = relationship(back_populates='target_users')

    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)
