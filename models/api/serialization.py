from __future__ import annotations

from collections.abc import Mapping
from typing import Any


def state_dict_schema_version(state: Mapping[str, Any]) -> str:
    raise NotImplementedError


def validate_state_dict(state: Mapping[str, Any], schema_version: str) -> None:
    raise NotImplementedError
