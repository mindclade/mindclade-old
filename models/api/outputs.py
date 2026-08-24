from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ModelOutputs:
    tensors: Mapping[str, Any]
    output_schema_version: str
