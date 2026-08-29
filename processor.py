from typing import Any, Dict, List, Set

class WalletProcessor:
    """Handles processing of cryptocurrency wallet transactions."""

    def __init__(self, address: str) -> None:
        """Initialize the wallet processor with an address."""
        self.address: str = address
        self.transactions: List[Dict[str, Any]] = []

    def add_transaction(self, transaction: Dict[str, Any]) -> bool:
        """Add a transaction if valid.

        Returns True if added, False otherwise.
        """
        if self._is_valid_transaction(transaction):
            self.transactions.append(transaction)
            return True
        return False

    def _is_valid_transaction(self, tx: Dict[str, Any]) -> bool:
        """Check if transaction has required fields and valid amount."""
        required_keys: List[str] = ["sender", "receiver", "amount", "asset"]
        if not all(key in tx for key in required_keys):
            return False
        amount = tx.get("amount")
        return isinstance(amount, (int, float)) and amount > 0

    def compute_balance(self, asset: str = "ETH") -> float:
        """Compute the balance for a specific asset."""
        balance: float = 0.0
        for tx in self.transactions:
            if tx.get("asset") != asset:
                continue
            if tx.get("receiver") == self.address:
                balance += float(tx["amount"])
            elif tx.get("sender") == self.address:
                balance -= float(tx["amount"])
        return balance

    def get_transaction_count(self) -> int:
        """Return the total number of transactions."""
        return len(self.transactions)

    def generate_report(self) -> Dict[str, Any]:
        """Generate a summary report of the wallet."""
        assets: Set[str] = {tx.get("asset", "UNKNOWN") for tx in self.transactions}
        report: Dict[str, Any] = {
            "wallet_address": self.address,
            "transaction_count": self.get_transaction_count(),
            "assets": list(assets),
            "balances": {asset: self.compute_balance(asset) for asset in assets}
        }
        return report