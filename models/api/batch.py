from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Batch:
    features: Mapping[str, Any]
    feature_schema_version: str
