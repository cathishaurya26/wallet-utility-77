import hashlib
import hmac
from functools import lru_cache
from typing import Tuple


class WalletCore:
    def __init__(self, seed: bytes):
        self.seed = seed
        self.master_key, self.master_chain_code = self._derive_master_node(seed)

    @staticmethod
    @lru_cache(maxsize=1024)
    def _derive_master_node(seed: bytes) -> Tuple[bytes, bytes]:
        out = hmac.new(b"Bitcoin seed", seed, hashlib.sha512).digest()
        return out[:32], out[32:]

    @staticmethod
    @lru_cache(maxsize=8192)
    def derive_child_node(
        parent_key: bytes, parent_chain_code: bytes, index: int
    ) -> Tuple[bytes, bytes]:
        is_hardened = index >= 0x80000000
        if is_hardened:
            data = b"\\x00" + parent_key + index.to_bytes(4, byteorder="big")
        else:
            data = parent_key + index.to_bytes(4, byteorder="big")

        out = hmac.new(parent_chain_code, data, hashlib.sha512).digest()
        return out[:32], out[32:]

    def derive_path(self