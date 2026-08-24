from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class Batch:
    features: Mapping[str, Any]
    feature_schema_version: str
