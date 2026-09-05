from decimal import Decimal, ROUND_HALF_UP
from typing import Union

class CryptoConverter:
    def __init__(self, precision: int = 8):
        self.precision = precision

    def to_decimal(self, amount: Union[str, float, int]) -> Decimal:
        return Decimal(str(amount)).quantize(
            Decimal(10) ** -self.precision, 
            rounding=ROUND_HALF_UP
        )

    def calculate_fee(self, amount: Decimal, rate: float) -> Decimal:
        return (amount * Decimal(str(rate))).quantize(
            Decimal(10) ** -self.precision, 
            rounding=ROUND_HALF_UP
        )

def format_address(address: str) -> str:
    if not address or len(address) < 10:
        return address
    return f"{address[:6]}...{address[-4:]}"

def validate_ticker(ticker: str) -> bool:
    if not isinstance(ticker, str):
        return False
    return 2 <= len(ticker) <= 8 and ticker.isalnum()