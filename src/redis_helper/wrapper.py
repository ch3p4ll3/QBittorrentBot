import logging
from pathlib import Path
from typing import Any, Optional

from .emulator import RedisEmulator

try:
    import redis.asyncio as redis
except ImportError:
    redis = None


class RedisWrapper:
    def __init__(self, url: Optional[str] = None, persist_path: Optional[Path] = None):
        """Unified Redis client that falls back to a persistent in-memory emulator when no URL is given."""
        self._url = url
        self._client = None
        self._emulator = RedisEmulator(persist_path=persist_path)

    async def connect(self):
        if not self._url or not redis:
            if self._emulator.persist_path:
                logging.warning(f"Redis disabled, using file-backed emulator ({self._emulator.persist_path})")
            else:
                logging.warning("Redis disabled, using in-memory emulator (data will not survive restarts)")
            self._client = self._emulator
            return

        try:
            client = redis.from_url(self._url, decode_responses=True)
            await client.ping()
            self._client = client
            logging.info("Connected to Redis")
        except Exception as e:
            if self._emulator.persist_path:
                logging.warning(f"Redis unavailable ({e}), falling back to file-backed emulator ({self._emulator.persist_path})")
            else:
                logging.warning(f"Redis unavailable ({e}), falling back to in-memory emulator (data will not survive restarts)")
            self._client = self._emulator

    # Unified API
    async def get(self, key: str) -> Optional[Any]:
        return await self._client.get(key)

    async def set(self, key: str, value: Any, ex: int | None = None):
        await self._client.set(key, value, ex=ex)

    async def delete(self, key: str):
        await self._client.delete(key)

    async def exists(self, key: str) -> bool:
        return await self._client.exists(key)
