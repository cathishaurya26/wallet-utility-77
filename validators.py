import re
from typing import Any, Dict

ETH_ADDRESS_REGEX = re.compile(r"^0x[a-fA-F0-9]{40}$")
BTC_ADDRESS_REGEX = re.compile(r"^(1|3|bc1)[a-zA-Z0-9]{25,39}$")


def is_valid_eth_address(address: str) -> bool:
    if not isinstance(address, str):
        return False
    return bool(ETH_ADDRESS_REGEX.match(address))


def is_valid_btc_address(address: str) -> bool:
    if not isinstance(address, str):
        return False
    return bool(BTC_ADDRESS_REGEX.match(address))


def validate_amount(amount: Any) -> bool:
    if isinstance(amount, (int, float)):
        return amount > 0
    if isinstance(amount, str):
        try:
            return float(amount) > 0
        except ValueError:
            return False
    return False


def validate_transaction_payload(payload: Dict[str, Any]) -> bool:
    required_fields = {"to_address", "amount", "currency"}
    if not isinstance(payload, dict) or not required_fields.issubset(payload.keys()):
        return False

    currency = str(payload.get("currency", "")).upper()
    address = payload.get("to_address")
    amount = payload.get("amount")

    if not validate_amount(amount):
        return False

    if currency == "ETH":
        return is_valid_eth_address(address)
    if currency == "BTC":
        return is_valid_btc_address(address)

    return bool(address and isinstance(address, str))
