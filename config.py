from typing import Dict, Any, Optional
import os

class WalletConfig:
    """Configuration management for wallet-utility-77."""

    def __init__(self, env: str = "production") -> None:
        self.env: str = env
        self.settings: Dict[str, Any] = self._load_settings()

    def _load_settings(self) -> Dict[str, Any]:
        """Retrieve base configuration settings."""
        return {
            "rpc_url": os.getenv("RPC_URL", "https://mainnet.infura.io/v3/"),
            "timeout": int(os.getenv("REQUEST_TIMEOUT", "30")),
            "retries": int(os.getenv("MAX_RETRIES", "3")),
            "debug": self.env == "development"
        }

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Access configuration value by key."""
        return self.settings.get(key, default)

    def validate(self) -> bool:
        """Check if critical configuration keys exist."""
        return "rpc_url" in self.settings

def get_config(env: Optional[str] = None) -> WalletConfig:
    """Factory function for configuration instantiation."""
    environment: str = env or os.getenv("APP_ENV", "production")
    return WalletConfig(env=environment)