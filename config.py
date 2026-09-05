import os
from typing import Dict, Any
from dataclasses import dataclass

@dataclass(frozen=True)
class WalletConfig:
    network: str
    rpc_url: str
    timeout: int

def load_network_config(network_name: str) -> WalletConfig:
    """Initialize configuration based on network selection."""
    configs: Dict[str, Dict[str, Any]] = {
        "mainnet": {"url": "https://mainnet.infura.io", "timeout": 30},
        "testnet": {"url": "https://sepolia.infura.io", "timeout": 15}
    }

    if network_name not in configs:
        raise ValueError(f"Unsupported network: {network_name}")

    settings = configs[network_name]
    return WalletConfig(
        network=network_name,
        rpc_url=settings["url"],
        timeout=settings["timeout"]
    )

def get_environment_variable(key: str, default: str = "") -> str:
    """Retrieve system environment variables with defaults."""
    return os.getenv(key, default)