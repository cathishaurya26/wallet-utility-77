import hashlib
import secrets
from typing import Optional

def generate_entropy(bits: int = 256) -> bytes:
    return secrets.token_bytes(bits // 8)

def compute_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def format_address(pubkey: bytes) -> str:
    return f"0x{pubkey.hex()}"

def validate_checksum(address: str) -> bool:
    if not address.startswith("0x") or len(address) != 66:
        return False
    return all(c in "0123456789abcdefABCDEF" for c in address[2:])

def truncate_address(address: str, length: int = 6) -> str:
    if len(address) <= length * 2:
        return address
    return f"{address[:length+2]}...{address[-length:]}"

def parse_amount(amount: str) -> float:
    try:
        return float(amount)
    except ValueError:
        return 0.0

def get_network_config(mainnet: bool = True) -> dict:
    return {
        "rpc_url": "https://mainnet.infura.io" if mainnet else "https://sepolia.infura.io",
        "chain_id": 1 if mainnet else 11155111
    }