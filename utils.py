import time
from typing import Any, Callable, Type

class NetworkError(Exception):
    pass

def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    exceptions: tuple[Type[Exception], ...] = (NetworkError,)
) -> Callable[[Callable], Callable]:
    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    if attempt == max_attempts:
                        raise NetworkError(
                            f"Failed after {max_attempts} attempts"
                        ) from exc
                    time.sleep(delay * (2 ** (attempt - 1)))
            return None
        return wrapper
    return decorator

def perform_network_operation(data: str) -> str:
    if len(data) < 5:
        raise NetworkError("Invalid data length")
    return f"Processed: {data}"

@retry(max_attempts=4, delay=0.1)
def safe_network_call(input_data: str) -> str:
    return perform_network_operation(input_data)

def fetch_crypto_price(symbol: str) -> float:
    try:
        result = safe_network_call(symbol)
        return 100.0
    except NetworkError:
        return 0.0

def get_transaction_count(address: str) -> int:
    try:
        result = safe_network_call(address)
        return 42
    except NetworkError as e:
        raise

def run_retry_test() -> bool:
    try:
        result = safe_network_call("validdata")
        return result == "Processed: validdata"
    except NetworkError:
        return False

if __name__ == "__main__":
    print(run_retry_test())