import asyncio
from typing import Any, Optional


class RedisEmulator:
    def __init__(self):
        self._storage: dict[str, Any] = {}
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[Any]:
        async with self._lock:
            return self._storage.get(key)

    async def set(self, key: str, value: Any, ex: int | None = None) -> None:
        async with self._lock:
            self._storage[key] = value

            if ex:
                asyncio.create_task(self._expire(key, ex))

    async def delete(self, key: str) -> None:
        async with self._lock:
            self._storage.pop(key, None)

    async def exists(self, key: str) -> bool:
        async with self._lock:
            return key in self._storage

    async def _expire(self, key: str, seconds: int):
        await asyncio.sleep(seconds)
        async with self._lock:
            self._storage.pop(key, None)
