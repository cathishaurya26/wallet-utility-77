import json
from decimal import Decimal
from typing import Any, Dict, List, Union

def normalize_address(address: str) -> str:
    address = address.strip()
    if address.startswith("0x"):
        address = address[2:]
    return "0x" + address.lower()

def convert_to_base_unit(amount: Union[int, str, float], decimals: int = 18) -> Decimal:
    if isinstance(amount, str):
        if amount.startswith("0x"):
            amount = int(amount, 16)
        else:
            amount = int(float(amount))
    elif isinstance(amount, float):
        amount = int(amount)
    return Decimal(amount) / (Decimal(10) ** decimals)

def is_valid_address(address: str) -> bool:
    if not address or not isinstance(address, str):
        return False
    normalized = normalize_address(address)
    if len(normalized) != 42:
        return False
    return all(c in "0123456789abcdef" for c in normalized[2:].lower())

def process_wallet_data(raw_input: str) -> Dict[str, Any]:
    try:
        data: Dict[str, Any] = json.loads(raw_input)
    except (json.JSONDecodeError, TypeError):
        return {"status": "error", "message": "Invalid input data"}
    result: Dict[str, Any] = {"status": "success"}
    if "address" in data:
        addr = data["address"]
        result["valid_address"] = is_valid_address(addr)
        if result["valid_address"]:
            result["normalized_address"] = normalize_address(addr)
        else:
            result["normalized_address"] = None
    if "transactions" in data and isinstance(data["transactions"], list):
        processed_txs: List[Dict[str, Any]] = []
        total_value = Decimal(0)
        for tx in data["transactions"]:
            if isinstance(tx, dict) and "value" in tx:
                val = convert_to_base_unit(tx["value"])
                total_value += val
                processed_txs.append({
                    "from": normalize_address(tx.get("from", "")),
                    "to": normalize_address(tx.get("to", "")),
                    "value": str(val)
                })
        result["transactions"] = processed_txs
        result["total_value"] = str(total_value)
    return result

def aggregate_balances(balances: List[Dict[str, Any]]) -> Dict[str, str]:
    agg: Dict[str, Decimal] = {}
    for bal in balances:
        if isinstance(bal, dict):
            asset = bal.get("asset", "unknown")
            dec = bal.get("decimals", 18)
            amt = convert_to_base_unit(bal.get("amount", 0), dec)
            if asset in agg:
                agg[asset] += amt
            else:
                agg[asset] = amt
    return {k: str(v) for k, v in agg.items()}