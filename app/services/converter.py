"""
Currency converter class
"""

import logging
import requests

from environs import Env

logger = logging.getLogger(__name__)

env = Env()
env.read_env()


class CurrencyConverter:
    """Currency converter class"""

    def __init__(self):

        self.base_url = (f'https://v6.exchangerate-api.com/v6/'
                         f'{env.str('RATE_API_KEY')}/pair')

    def convert(self, source, target, amount) -> float:
        """Converts the amount from source currency to target currency."""

        r = requests.get(f'{self.base_url}/{source}/{target}/{amount}')

        if r.status_code != 200:
            logger.error('Convertion request failed.')
            raise Exception(f'Convertion request failed.')
        else:
            data = r.json()
            return float(data['conversion_result'])
