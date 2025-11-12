def get_exchange_message(
        source_sum: int | float,
        target_sum: int | float,
        user_id: str | int,
        db: dict[str, dict[str, dict[str, str] | str]]
) -> str:
    """Get text message for main exchange window."""

    text = (f'{db['users'][user_id]['source']}  '
            f'<b>{source_sum:,.2f}</b>    ➡️    '
            f'{db['users'][user_id]['target']}  '
            f'<b>{target_sum:,.2f}</b>\n\n\n'.replace(',', ' '))

    return text
