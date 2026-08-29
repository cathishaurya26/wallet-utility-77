import hashlib
import os
from typing import Dict, Optional

class WalletHandler:
    def __init__(self, network: str = "mainnet") -> None:
        self.network = network
        self.wallets: Dict[str, Dict[str, str]] = {}

    def create_wallet(self, name: str) -> str:
        if name in self.wallets:
            raise ValueError("wallet already exists")
        seed = os.urandom(32)
        private_key = hashlib.sha256(seed).hexdigest()
        address = "0x" + hashlib.sha256(private_key.encode()).hexdigest()[:40]
        self.wallets[name] = {"private_key": private_key, "address": address}
        return address

    def get_balance(self, name: str) -> float:
        if name not in self.wallets:
            return 0.0
        address = self.wallets[name]["address"]
        balance = int(address[2:10], 16) / 1e8
        return balance

    def transfer(self, from_name: str, to_address: str, amount: float) -> str:
        if from_name not in self.wallets:
            raise ValueError("sender wallet not found")
        if amount <= 0:
            raise ValueError("invalid amount")
        private_key = self.wallets[from_name]["private_key"]
        tx_data = f"{from_name}:{to_address}:{amount}"
        signature = hashlib.sha256((private_key + tx_data).encode()).hexdigest()
        return signature

    def get_wallet_info(self, name: str) -> Optional[Dict[str, str]]:
        return self.wallets.get(name)
