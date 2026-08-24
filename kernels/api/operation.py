from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class KernelImplementation(Protocol):
    name: str
    version: str

    def __call__(self, *args, **kwargs): ...


@dataclass(frozen=True)
class Operation:
    name: str
    reference: KernelImplementation
    implementations: tuple[KernelImplementation, ...]
