from typing import Tuple
import requests
from langsmith import traceable
from src.core.config import EXCHANGERATE_API_KEY


@traceable(name="get_exchange_rate", description="Get the exchange rate and convert an amount from one currency to another.")
def get_exchange_rate(base: str, target: str, amount: str) -> Tuple:
    """Return a tuple of (base, target, amount, conversion_result (2 decimal places))"""
    response = requests.get(
        f"https://v6.exchangerate-api.com/v6/{EXCHANGERATE_API_KEY}/pair/{base}/{target}/{amount}"
    )
    if response.status_code == 200:
        data = response.json()
        conversion_result = round(data["conversion_result"], 2)
        return base, target, amount, conversion_result
    else:
        raise Exception(
            f"Error fetching exchange rate: {response.status_code} - {response.text}"
        )
