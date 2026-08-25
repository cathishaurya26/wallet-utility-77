import hashlib
from typing import List, Dict, Any

class Processor:
    def __init__(self) -> None:
        self._cache: Dict[str, Dict[str, Any]] = {}

    def process_wallets(self, wallets: List[str]) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        for wallet in wallets:
            if wallet in self._cache:
                results.append(self._cache[wallet])
                continue
            processed = self._compute_wallet(wallet)
            self._cache[wallet] = processed
            results.append(processed)
        return results

    def _compute_wallet(self, wallet: str) -> Dict[str, Any]:
        data = wallet.encode("utf-8")
        hash_val = hashlib.sha256(data).hexdigest()
        balance = int(hash_val[:16], 16) % 1000000000
        return {"address": wallet, "balance": balance, "hash": hash_val[:10]}

    def deduplicate_and_process(self, wallets: List[str]) -> List[Dict[str, Any]]:
        seen = set()
        unique = []
        for w in wallets:
            if w not in seen:
                seen.add(w)
                unique.append(w)
        return self.process_wallets(unique)

    def clear_cache(self) -> None:
        self._cache.clear()