from __future__ import annotations


class CheckpointManager:
    def save(self, state, *, blocking: bool = False) -> str:
        raise NotImplementedError

    def load(self, checkpoint_ref: str, *, components: list[str] | None = None):
        raise NotImplementedError

    def latest_committed(self) -> str | None:
        raise NotImplementedError
