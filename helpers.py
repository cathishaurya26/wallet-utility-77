import re
from decimal import Decimal

def validate_address(address):
    if not isinstance(address, str):
        return False
    if len(address) < 26 or len(address) > 35:
        return False
    pattern = r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$'
    return re.match(pattern, address) is not None

def validate_amount(amount_str):
    try:
        amount = Decimal(amount_str)
        return amount > 0
    except (ValueError, TypeError):
        return False

def process_wallet_operation(address, amount_str):
    if not validate_address(address):
        return False, "invalid address format"
    if not validate_amount(amount_str):
        return False, "invalid amount"
    amount = Decimal(amount_str)
    print(f"validating transaction to {address} for {amount} btc")
    return True, "operation processed"

def main_processing_loop():
    print("starting wallet utility")
    while True:
        address = input("address: ").strip()
        if address == "exit":
            print("exiting")
            break
        amount_str = input("amount: ").strip()
        success, message = process_wallet_operation(address, amount_str)
        if success:
            print(message)
        else:
            print("error:", message)

if __name__ == "__main__":
    main_processing_loop()