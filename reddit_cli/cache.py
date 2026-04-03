"""Simple file-based caching for Reddit API responses."""
import json
import hashlib
import os
from pathlib import Path
from typing import Any
from datetime import datetime, timedelta

# Cache directory location
CACHE_DIR = Path.home() / ".cache" / "reddit_cli"
CACHE_TTL_MINUTES = 5


def _get_cache_file_path(endpoint: str, params: dict | None = None) -> Path:
    """Generate a cache file path based on endpoint and params.

    Args:
        endpoint: API endpoint path
        params: Query parameters dict

    Returns:
        Path to the cache file
    """
    # Create a unique key based on endpoint and params
    key_parts = [endpoint]
    if params:
        # Sort params for consistent hashing
        for k, v in sorted(params.items()):
            key_parts.append(f"{k}={v}")
    key_string = ":".join(key_parts)
    key_hash = hashlib.md5(key_string.encode()).hexdigest()

    # Create cache directory if it doesn't exist
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    return CACHE_DIR / f"{key_hash}.json"


def _is_cache_valid(cache_file: Path) -> bool:
    """Check if a cache file is still valid based on TTL.

    Args:
        cache_file: Path to the cache file

    Returns:
        True if cache is valid, False otherwise
    """
    if not cache_file.exists():
        return False

    try:
        with open(cache_file, "r") as f:
            cache_data = json.load(f)

        cached_time = datetime.fromisoformat(cache_data["timestamp"])
        expiry_time = cached_time + timedelta(minutes=CACHE_TTL_MINUTES)

        return datetime.now() < expiry_time
    except (json.JSONDecodeError, KeyError, ValueError):
        # Cache is invalid if we can't read or parse it
        return False


def get_cached(endpoint: str, params: dict | None = None) -> dict | None:
    """Get cached response if available and valid.

    Args:
        endpoint: API endpoint path
        params: Query parameters dict

    Returns:
        Cached response dict if valid, None otherwise
    """
    cache_file = _get_cache_file_path(endpoint, params)

    if not _is_cache_valid(cache_file):
        return None

    try:
        with open(cache_file, "r") as f:
            cache_data = json.load(f)
        return cache_data.get("response")
    except (json.JSONDecodeError, KeyError):
        return None


def set_cached(endpoint: str, params: dict | None, response: dict) -> None:
    """Store response in cache.

    Args:
        endpoint: API endpoint path
        params: Query parameters dict
        response: API response dict to cache
    """
    cache_file = _get_cache_file_path(endpoint, params)

    cache_data = {
        "endpoint": endpoint,
        "params": params,
        "response": response,
        "timestamp": datetime.now().isoformat(),
    }

    try:
        with open(cache_file, "w") as f:
            json.dump(cache_data, f)
    except OSError:
        # Silently fail if we can't write to cache
        pass


def clear_cache() -> None:
    """Clear all cached responses."""
    if CACHE_DIR.exists():
        for cache_file in CACHE_DIR.glob("*.json"):
            try:
                cache_file.unlink()
            except OSError:
                pass


def get_cache_size() -> int:
    """Get the number of cached items.

    Returns:
        Number of cached items
    """
    if not CACHE_DIR.exists():
        return 0
    return len(list(CACHE_DIR.glob("*.json")))
