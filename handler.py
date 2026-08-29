import json
import hashlib
from dataclasses import dataclass, asdict
from typing import List, Dict, Any

@dataclass
class Transaction:
    tx_id: str
    amount: float
    address: str
    timestamp: int

def parse_raw_data(raw_json: str) -> List[Dict[str, Any]]:
    try:
        return json.loads(raw_json)
    except (json.JSONDecodeError, TypeError):
        return []

def create_transactions(data_list: List[Dict[str, Any]]) -> List[Transaction]:
    transactions: List[Transaction] = []
    for item in data_list:
        if isinstance(item, dict) and all(k in item for k in ['tx_id', 'amount', 'address', 'timestamp']):
            try:
                tx = Transaction(
                    tx_id=str(item['tx_id']),
                    amount=float(item['amount']),
                    address=str(item['address']),
                    timestamp=int(item['timestamp'])
                )
                transactions.append(tx)
            except (ValueError, TypeError):
                continue
    return transactions

def validate_address(address: str) -> bool:
    if not isinstance(address, str) or len(address) < 26 or len(address) > 35:
        return False
    valid_chars = set('123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz')
    return all(c in valid_chars for c in address)

def filter_valid_transactions(transactions: List[Transaction]) -> List[Transaction]:
    return [tx for tx in transactions if validate_address(tx.address) and tx.amount > 0]

def compute_hash(data: str) -> str:
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def process_wallet(wallet: Dict[str, Any]) -> Dict[str, Any]:
    if 'transactions' not in wallet:
        wallet['transactions'] = []
    wallet['tx_count'] = len(wallet['transactions'])
    wallet['checksum'] = compute_hash(json.dumps(wallet, sort_keys=True))
    return wallet

def handle_crypto_data(raw_data: str) -> str:
    parsed_data = parse_raw_data(raw_data)
    transactions = create_transactions(parsed_data)
    valid_transactions = filter_valid_transactions(transactions)
    result = {
        'valid_transactions': [asdict(tx) for tx in valid_transactions],
        'total_count': len(valid_transactions),
        'invalid_count': len(transactions) - len(valid_transactions)
    }
    return json.dumps(result, indent=2)