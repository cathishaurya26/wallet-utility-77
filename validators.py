import re
from typing import Union


class WalletValidator:
    """Validates cryptocurrency wallet addresses and transaction inputs."""

    ETH_ADDRESS_PATTERN = re.compile(r"^0x[a-fA-F0-9]{40}$")
    BTC_ADDRESS_PATTERN = re.compile(r"^(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}$")

    @classmethod
    def is_valid_eth_address(cls, address: str) -> bool:
        """Check if the provided string is a valid Ethereum address.

        Args:
            address: The wallet address string to validate.

        Returns:
            True if valid format, False otherwise.
        """
        if not isinstance(address, str):
            return False
        return bool(cls.ETH_ADDRESS_PATTERN.match(address))

    @classmethod
    def is_valid_btc_address(cls, address: str) -> bool:
        """Check if the provided string is a valid Bitcoin address.

        Args:
            address: The wallet address string to validate.

        Returns:
            True if valid format, False otherwise.
        """
        if not isinstance(address, str):
            return False
        return bool(cls.BTC_ADDRESS_PATTERN.match(address))

    @staticmethod
    def validate_amount(amount: Union[int, float], min_value: float = 0.0001) -> bool:
        """Validate transaction amount against minimum operational limits.

        Args:
            amount: Numeric transfer value to verify.
            min_value: Minimum allowed value for the transaction.

        Returns:
            True if amount is numeric and exceeds minimum threshold.
        """
        if not isinstance(amount, (int, float)) or isinstance(amount, bool):
            return False
        return amount >= min_value
