from __future__ import annotations

from typing import Any, Mapping, Protocol


class Checkpointable(Protocol):
    def state_dict(self) -> Mapping[str, Any]: ...

    def load_state_dict(self, state: Mapping[str, Any]) -> None: ...
