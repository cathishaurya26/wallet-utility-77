import os
from typing import Any, Dict

DEFAULT_CONFIG = {
    "NETWORK": "mainnet",
    "RPC_TIMEOUT": 30,
    "MAX_RETRIES": 3,
    "KEY_PATH": "./keys/"
}

class ConfigLoader:
    def __init__(self, overrides: Dict[str, Any] = None):
        self.settings = DEFAULT_CONFIG.copy()
        if overrides:
            self.settings.update(overrides)

    def get(self, key: str) -> Any:
        return self.settings.get(key, os.getenv(key))

def load_config() -> ConfigLoader:
    env_overrides = {
        "NETWORK": os.getenv("WALLET_NETWORK"),
        "RPC_TIMEOUT": int(os.getenv("WALLET_TIMEOUT", 30))
    }
    return ConfigLoader({k: v for k, v in env_overrides.items() if v is not None})