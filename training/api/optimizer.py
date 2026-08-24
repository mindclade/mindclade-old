from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True)
class OptimizerContext:
    topology: Any
    precision_policy: Any
    parameter_groups: Sequence[Any]


class OptimizerFactory(Protocol):
    def build(self, model, context: OptimizerContext): ...
