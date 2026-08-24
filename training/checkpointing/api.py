from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Protocol


class Checkpointable(Protocol):
    def state_dict(self) -> Mapping[str, Any]: ...

    def load_state_dict(self, state: Mapping[str, Any]) -> None: ...
