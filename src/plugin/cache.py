import os
import time
import json
import functools
from typing import Callable


def is_file_outdated(file_path: str, seconds: int = 300) -> bool:
    """Check if a file is outdated.

    Args:
        file_path (str): The path to the file.
        seconds (int, optional): How old the file may be. Defaults to 300.

    Returns:
        bool: True if the file is outdated, False otherwise.
    """
    if not os.path.exists(file_path):
        return True
    return time.time() - os.path.getmtime(file_path) > seconds


def cache(
    freshness: int = 300,
    cache_path: str = ".cache.json",
) -> Callable:
    """Cache the result of a function.

    Args:
        freshness (int, optional): The number of seconds to keep the cache. Defaults to 300.
        cache_path (str, optional): The file to store the cache in. Defaults to ".cache.json".

    Returns:
        Callable: The decorated function.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if is_file_outdated(cache_path, freshness):
                result = func(*args, **kwargs)
                with open(cache_path, "w") as f:
                    json.dump(result, f)
            else:
                with open(cache_path, "r") as f:
                    result = json.load(f)
            return result

        return wrapper

    return decorator
