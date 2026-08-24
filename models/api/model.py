from __future__ import annotations

from typing import Mapping, Protocol


class Model(Protocol):
    def forward(self, batch: Batch) -> ModelOutputs: ...

    def state_schema(self) -> Mapping[str, str]: ...

    def capabilities(self) -> ModelCapabilities: ...
