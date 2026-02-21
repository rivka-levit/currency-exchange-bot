from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Currency

CURRENCIES = {
    'AED': 'United Arab Emirates Dirham',
    'ARS': 'Argentine Peso',
    'AUD': 'Australian Dollar',
    'BWP': 'Botswanan Pula',
    'BGN': 'Bulgarian Lev',
    'BHD': 'Bahraini Dinar',
    'BND': 'Brunei Dollar',
    'BRL': 'Brazilian Real',
    'CAD': 'Canadian Dollar',
    'CHF': 'Swiss Franc',
    'CLP': 'Chilean Peso',
    'CNY': 'Chinese Yuan',
    'COP': 'Colombian Peso',
    'CZK': 'Czech Republic Koruna',
    'DKK': 'Danish Krone',
    'EUR': 'Euro',
    'GBP': 'British Pound Sterling',
    'HKD': 'Hong Kong Dollar',
    'HRK': 'Croatian Kuna',
    'HUF': 'Hungarian Forint',
    'IDR': 'Indonesian Rupiah',
    'ILS': 'Israeli New Sheqel',
    'INR': 'Indian Rupee',
    'IRR': 'Iranian Rial',
    'ISK': 'Icelandic Krona',
    'JPY': 'Japanese Yen',
    'KRW': 'South Korean Won',
    'KWD': 'Kuwaiti Dinar',
    'KZT': 'Kazakhstani Tenge',
    'LKR': 'Sri Lankan Rupee',
    'LYD': 'Libyan Dinar',
    'MUR': 'Mauritian Rupee',
    'MXN': 'Mexican Peso',
    'MYR': 'Malaysian Ringgit',
    'NOK': 'Norwegian Krone',
    'NPR': 'Nepalese Rupee',
    'NZD': 'New Zealand Dollar',
    'OMR': 'Omani Rial',
    'PHP': 'Philippine Peso',
    'PKR': 'Pakistani Rupee',
    'PLN': 'Polish Zloty',
    'QAR': 'Qatari Rial',
    'RON': 'Romanian Leu',
    'RUB': 'Russian Ruble',
    'SAR': 'Saudi Riyal',
    'SEK': 'Swedish Krona',
    'SGD': 'Singapore Dollar',
    'THB': 'Thai Baht',
    'TRY': 'Turkish Lira',
    'TTD': 'Trinidad and Tobago Dollar',
    'TWD': 'New Taiwan Dollar',
    'USD': 'United States Dollar',
    'VEF': 'Venezuelan Bolivar Fuerte',
    'ZAR': 'South African Rand'
}


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
