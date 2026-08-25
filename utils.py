import re
import secrets

def wei_to_ether(wei: int) -> float:
    return wei / 10 ** 18

def ether_to_wei(ether: float) -> int:
    return int(ether * 10 ** 18)

def satoshi_to_btc(satoshi: int) -> float:
    return satoshi / 10 ** 8

def btc_to_satoshi(btc: float) -> int:
    return int(btc * 10 ** 8)

def is_valid_address(address: str) -> bool:
    if not isinstance(address, str):
        return False
    pattern = r'^0x[0-9a-fA-F]{40}$'
    return bool(re.match(pattern, address))

def format_balance(balance: int, decimals: int = 18) -> str:
    if decimals <= 0:
        return str(balance)
    divisor = 10 ** decimals
    whole = balance // divisor
    fraction = balance % divisor
    fraction_str = f"{fraction:0{decimals}d}".rstrip('0')
    if fraction_str:
        return f"{whole}.{fraction_str}"
    return str(whole)

def truncate_address(address: str, prefix_len: int = 6, suffix_len: int = 4) -> str:
    if not is_valid_address(address):
        return address
    return f"{address[:prefix_len]}...{address[-suffix_len:]}"

def generate_private_key() -> str:
    return secrets.token_hex(32)

def is_valid_private_key(key: str) -> bool:
    if not isinstance(key, str):
        return False
    return bool(re.match(r'^[0-9a-fA-F]{64}$', key))