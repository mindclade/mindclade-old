from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol, Sequence


@dataclass(frozen=True)
class OptimizerContext:
    topology: Any
    precision_policy: Any
    parameter_groups: Sequence[Any]


class OptimizerFactory(Protocol):
    def build(self, model, context: OptimizerContext): ...
