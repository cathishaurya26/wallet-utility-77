import re
from typing import Optional

def is_valid_ethereum_address(address: str) -> bool:
    if not isinstance(address, str) or len(address) == 0:
        return False
    if not address.startswith("0x"):
        return False
    addr = address[2:]
    if len(addr) != 40:
        return False
    return bool(re.match(r"^[0-9a-fA-F]{40}$", addr))

def is_valid_bitcoin_address(address: str) -> bool:
    if not isinstance(address, str) or len(address) == 0:
        return False
    if re.match(r"^(1|3)[a-km-zA-HJ-NP-Z1-9]{25,34}$", address):
        return True
    if re.match(r"^bc1[a-z0-9]{39,59}$", address):
        return True
    return False

def is_valid_private_key(key: str) -> bool:
    if not isinstance(key, str) or len(key) == 0:
        return False
    key = key.lower().replace("0x", "")
    if len(key) != 64:
        return False
    return bool(re.match(r"^[0-9a-f]{64}$", key))

def is_valid_amount(amount: float) -> bool:
    if not isinstance(amount, (int, float)):
        return False
    return amount > 0

def is_valid_transaction_amount(amount: str, max_amount: Optional[float] = None) -> bool:
    try:
        amt = float(amount)
        if amt <= 0:
            return False
        if max_amount is not None and amt > max_amount:
            return False
        return True
    except (ValueError, TypeError):
        return False

def validate_address(address: str, chain: str = "ethereum") -> bool:
    if chain == "ethereum":
        return is_valid_ethereum_address(address)
    elif chain == "bitcoin":
        return is_valid_bitcoin_address(address)
    return False