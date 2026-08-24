from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RetentionPolicy:
    keep_last: int
    keep_every_n_steps: int | None
    pinned: tuple[str, ...]


def apply(policy: RetentionPolicy, checkpoints: list[str]) -> list[str]:
    raise NotImplementedError
