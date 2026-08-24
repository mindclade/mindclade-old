from __future__ import annotations


class AsyncSaver:
    def __init__(self, *, staging_memory_bytes: int) -> None:
        self.staging_memory_bytes = staging_memory_bytes

    def submit(self, plan) -> None:
        raise NotImplementedError

    def drain(self) -> None:
        raise NotImplementedError
