import asyncio
import json
import time
import logging
import tempfile
from pathlib import Path
from typing import Any, Optional


class RedisEmulator:
    def __init__(self, persist_path: Optional[Path] = None):
        """In-memory Redis emulator with optional JSON persistence across restarts."""
        self._storage: dict[str, dict[str, Any]] = {}
        self._lock = asyncio.Lock()
        self._persist_path = persist_path
        self._load()

    @property
    def persist_path(self) -> Optional[Path]:
        return self._persist_path

    def _load(self):
        if not self._persist_path or not self._persist_path.exists():
            return

        try:
            with open(self._persist_path, "r", encoding="utf-8") as f:
                raw = json.load(f)

            now = time.time()
            normalized = {}
            for k, v in raw.items():
                # accept both the current {"value":…,"expires_at":…} shape and
                # any older flat {key: value} shape written by a previous version
                if not isinstance(v, dict) or "value" not in v:
                    v = {"value": v, "expires_at": None}
                if v.get("expires_at") is None or v["expires_at"] > now:
                    normalized[k] = v
            self._storage = normalized
        except Exception as e:
            logging.exception(f"Could not load emulator state from disk: {e}")

    def _save(self, snapshot: dict) -> None:
        if not self._persist_path:
            return

        try:
            self._persist_path.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(
                "w", encoding="utf-8", dir=self._persist_path.parent, delete=False, suffix=".tmp"
            ) as f:
                json.dump(snapshot, f)
                tmp = Path(f.name)
            tmp.replace(self._persist_path)
        except Exception as e:
            logging.exception(f"Could not persist emulator state to disk: {e}")

    async def get(self, key: str) -> Optional[Any]:
        snapshot = None
        async with self._lock:
            entry = self._storage.get(key)
            if entry is None:
                return None
            expires_at = entry.get("expires_at")
            if expires_at is not None and time.time() > expires_at:
                self._storage.pop(key)
                snapshot = dict(self._storage)
            else:
                return entry["value"]
        self._save(snapshot)
        return None

    async def set(self, key: str, value: Any, ex: int | None = None) -> None:
        async with self._lock:
            expires_at = time.time() + ex if ex is not None and ex > 0 else None
            self._storage[key] = {"value": value, "expires_at": expires_at}
            snapshot = dict(self._storage)
        self._save(snapshot)
        if ex is not None and ex > 0:
            asyncio.create_task(self._expire(key, expires_at))

    async def delete(self, key: str) -> None:
        async with self._lock:
            self._storage.pop(key, None)
            snapshot = dict(self._storage)
        self._save(snapshot)

    async def exists(self, key: str) -> bool:
        snapshot = None
        async with self._lock:
            entry = self._storage.get(key)
            if entry is None:
                return False
            expires_at = entry.get("expires_at")
            if expires_at is not None and time.time() > expires_at:
                self._storage.pop(key, None)
                snapshot = dict(self._storage)
                result = False
            else:
                result = True
        if snapshot is not None:
            self._save(snapshot)
        return result

    async def _expire(self, key: str, expires_at: float):
        await asyncio.sleep(max(0, expires_at - time.time()))
        snapshot = None
        async with self._lock:
            entry = self._storage.get(key)
            if entry is not None and entry.get("expires_at") == expires_at:
                self._storage.pop(key)
                snapshot = dict(self._storage)
        if snapshot is not None:
            self._save(snapshot)
