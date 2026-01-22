import asyncio
import qbittorrentapi
from typing import Any, Callable


class AsyncQbittorrentClient:
    """
    Async wrapper around qbittorrentapi.Client using asyncio.to_thread.
    """

    def __init__(self, **connection_kwargs):
        self._connection_kwargs = connection_kwargs
        self._client: qbittorrentapi.Client | None = None

    async def __aenter__(self) -> "AsyncQbittorrentClient":
        self._client = qbittorrentapi.Client(**self._connection_kwargs)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        # qbittorrentapi.Client has no async close, but keep hook for symmetry
        self._client = None

    async def call(self, fn: Callable[..., Any], /, *args, **kwargs) -> Any:
        """
        Run a qbittorrentapi call in a thread.
        """
        if not self._client:
            raise RuntimeError("Client not initialized, use 'async with'")

        return await asyncio.to_thread(fn, *args, **kwargs)

    @property
    def client(self) -> qbittorrentapi.Client:
        if not self._client:
            raise RuntimeError("Client not initialized, use 'async with'")
        return self._client
