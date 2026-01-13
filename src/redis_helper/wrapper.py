import logging
from typing import Any, Optional

from .emulator import RedisEmulator

try:
    import redis.asyncio as redis
except ImportError:
    redis = None


class RedisWrapper:
    def __init__(self, url: Optional[str] = None):
        self._url = url
        self._client = None
        self._emulator = RedisEmulator()

    async def connect(self):
        if not self._url or not redis:
            logging.warning("Redis disabled. using in-memory storage")
            self._client = self._emulator
            return

        try:
            client = redis.from_url(self._url, decode_responses=True)
            await client.ping()
            self._client = client
            logging.info("Connected to Redis")
        except Exception as e:
            logging.warning(f"Redis unavailable ({e}), using in-memory storage")
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
