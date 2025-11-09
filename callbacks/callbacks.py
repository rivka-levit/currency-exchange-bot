from aiogram.filters.callback_data import CallbackData


class SourceCurrencyCallbackFactory(CallbackData, prefix='source'):
    """Source currency callback factory."""

    code: str
    name: str


class TargetCurrencyCallbackFactory(CallbackData, prefix='target'):
    """Target currency callback factory."""

    code: str
    name: str
