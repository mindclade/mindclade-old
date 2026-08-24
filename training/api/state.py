from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any


@dataclass
class TrainingState:
    step: int
    tokens_seen: int
    examples_seen: int
    checkpointables: Mapping[str, Any]
    rng_streams: Mapping[str, Any]
