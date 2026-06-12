import asyncio
import json
import time
import logging
from pathlib import Path
from typing import Any, Optional


class RedisEmulator:
    def __init__(self, persist_path: Optional[Path] = None):
        self._storage: dict[str, dict] = {}
        self._lock = asyncio.Lock()
        self._persist_path = persist_path
        self._load()

    def _load(self):
        if not self._persist_path or not self._persist_path.exists():
            return

        try:
            with open(self._persist_path, "r") as f:
                raw = json.load(f)

            now = time.time()
            self._storage = {
                k: v for k, v in raw.items()
                if v.get("expires_at") is None or v["expires_at"] > now
            }
        except Exception as e:
            logging.warning(f"Could not load emulator state from disk: {e}")

    def _save(self):
        if not self._persist_path:
            return

        try:
            self._persist_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self._persist_path, "w") as f:
                json.dump(self._storage, f)
        except Exception as e:
            logging.warning(f"Could not persist emulator state to disk: {e}")

    async def get(self, key: str) -> Optional[Any]:
        async with self._lock:
            entry = self._storage.get(key)
            if entry is None:
                return None
            return entry["value"]

    async def set(self, key: str, value: Any, ex: int | None = None) -> None:
        async with self._lock:
            expires_at = time.time() + ex if ex else None
            self._storage[key] = {"value": value, "expires_at": expires_at}
            self._save()

        if ex:
            asyncio.create_task(self._expire(key, ex))

    async def delete(self, key: str) -> None:
        async with self._lock:
            self._storage.pop(key, None)
            self._save()

    async def exists(self, key: str) -> bool:
        async with self._lock:
            entry = self._storage.get(key)
            if entry is None:
                return False
            expires_at = entry.get("expires_at")
            if expires_at is not None and time.time() > expires_at:
                self._storage.pop(key, None)
                self._save()
                return False
            return True

    async def _expire(self, key: str, seconds: int):
        await asyncio.sleep(seconds)
        async with self._lock:
            self._storage.pop(key, None)
            self._save()
