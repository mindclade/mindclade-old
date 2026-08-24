from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Capability:
    dtypes: tuple[str, ...]
    shape_families: tuple[str, ...]
    layouts: tuple[str, ...]
    device_architectures: tuple[str, ...]
    supports_gradients: bool
    deterministic: bool

    def admits(self, signature) -> bool:
        raise NotImplementedError
