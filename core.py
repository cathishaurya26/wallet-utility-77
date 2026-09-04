from decimal import Decimal, ROUND_HALF_UP
from typing import Optional

class CryptoConverter:
    def __init__(self, precision: int = 8):
        self.precision = precision

    def format_amount(self, value: float) -> str:
        """Formats float values to specific precision."""
        quantize_str = '1.' + '0' * self.precision
        amount = Decimal(str(value)).quantize(Decimal(quantize_str), rounding=ROUND_HALF_UP)
        return format(amount, f'.{self.precision}f')

    @staticmethod
    def validate_address(address: str, chain: str) -> bool:
        """Simple validation for crypto addresses."""
        if chain == 'btc':
            return len(address) in range(26, 36) and address.isalnum()
        if chain == 'eth':
            return len(address) == 42 and address.startswith('0x')
        return False

    def calculate_fee(self, amount: float, rate: float) -> Decimal:
        """Calculates network transaction fee."""
        return Decimal(str(amount)) * Decimal(str(rate))

    def safe_parse(self, data: Optional[str]) -> Decimal:
        """Safe parsing for string inputs."""
        try:
            return Decimal(data or '0')
        except Exception:
            return Decimal('0')