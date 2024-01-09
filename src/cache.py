import os
import time
import json
import functools
from typing import Callable


def is_file_outdated(file_path: str, minutes: int = 5) -> bool:
    """Check if a file is outdated.

    Args:
        file_path (str): The path to the file.
        minutes (int, optional): The number of minutes to check. Defaults to 5.

    Returns:
        bool: True if the file is outdated, False otherwise.
    """
    if not os.path.exists(file_path):
        return True
    return (time.time() - os.path.getmtime(file_path)) / 60 > minutes


def cache(
    freshness: int = 300,
    cache_path: str = ".cache.json",
) -> Callable:
    """Cache the result of a function.

    Args:
        freshness (int, optional): The number of seconds to keep the cache. Defaults to 300.
        cache_dir (str, optional): The directory to store the cache. Defaults to "cache".
        cache_file (str, optional): The name of the cache file. Defaults to "cache.json".
        cache_key (Optional[str], optional): The key to use for the cache. Defaults to None.

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
