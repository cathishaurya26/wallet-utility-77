import hashlib
import json
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Transaction:
    sender: str
    recipient: str
    amount: float
    signature: str = ""

@dataclass
class Wallet:
    address: str
    balance: float = 0.0
    transactions: List[Transaction] = field(default_factory=list)

    def generate_key_pair(self) -> Dict[str, str]:
        private = hashlib.sha256(self.address.encode()).hexdigest()
        public = hashlib.sha256(private.encode()).hexdigest()
        return {"private": private, "public": public}

    def sign(self, tx: Transaction, private_key: str) -> str:
        data = f"{tx.sender}{tx.recipient}{tx.amount}{private_key}"
        return hashlib.sha256(data.encode()).hexdigest()

    def add_transaction(self, tx: Transaction):
        self.transactions.append(tx)
        self.balance -= tx.amount

    def get_balance(self) -> float:
        return self.balance

def create_new_wallet(address: str) -> Wallet:
    return Wallet(address=address)

def process_transfer(from_wallet: Wallet, to_wallet: Wallet, amount: float, private_key: str) -> bool:
    if from_wallet.balance < amount:
        return False
    tx = Transaction(
        sender=from_wallet.address,
        recipient=to_wallet.address,
        amount=amount
    )
    signature = from_wallet.sign(tx, private_key)
    tx.signature = signature
    from_wallet.add_transaction(tx)
    to_wallet.balance += amount
    to_wallet.add_transaction(tx)
    return True

def serialize_wallet(wallet: Wallet) -> str:
    data = {
        "address": wallet.address,
        "balance": wallet.balance,
        "transactions": [
            {
                "sender": t.sender,
                "recipient": t.recipient,
                "amount": t.amount,
                "signature": t.signature
            } for t in wallet.transactions
        ]
    }
    return json.dumps(data, indent=2)