"""
Tests for services of the app.
"""

import pytest

from exceptions import ConversionRequestError
from services.converter import CurrencyConverter


def test_currency_convertion_success():
    """Test currency convertion success."""

    cnv = CurrencyConverter()
    source = 'USD'
    target = 'EUR'
    amount = 100

    result = cnv.convert(source, target, amount)

    assert isinstance(result, float)


def test_invalid_currency_request_fails():
    """Test currency request fails with invalid currency code."""

    cnv = CurrencyConverter()

    source = 'USD'
    target = 'PPP'
    amount = 100

    with pytest.raises(ConversionRequestError):
        cnv.convert(source, target, amount)
