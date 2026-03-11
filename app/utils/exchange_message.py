def get_exchange_message(
        source_sum: int | float,
        target_sum: int | float,
        source_cur: str,
        target_cur: str
) -> str:
    """Get text exchange message."""

    text = (f'［{source_cur}］<b>{source_sum:,.2f}</b>  ➡️  '
            f'<b>{target_sum:,.2f}</b>［{target_cur}］'.replace(',', ' '))

    return text
