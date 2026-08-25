# wallet-utility-77

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

wallet-utility-77 is a Python library for cryptocurrency wallet operations. It allows developers to generate wallets, derive addresses for different blockchains, and perform key management tasks securely.

## Features
- Generate and validate BIP39 mnemonic phrases with 12 or 24 words
- Derive Ethereum and Bitcoin addresses using standard derivation paths
- Perform offline private key to address conversions
- Check Ethereum wallet balances via integrated JSON-RPC support

## Installation

```bash
git clone https://github.com/Developer/wallet-utility-77.git
cd wallet-utility-77
pip install -r requirements.txt
```

## Usage

```python
from wallet_utility_77 import Wallet

wallet = Wallet.generate()
print("ETH address:", wallet.get_address("ethereum"))
print("Mnemonic:", wallet.mnemonic)
```

## License

MIT