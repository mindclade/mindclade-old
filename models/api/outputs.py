from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class ModelOutputs:
    tensors: Mapping[str, Any]
    output_schema_version: str
