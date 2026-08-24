from __future__ import annotations

from typing import Any, Mapping


def state_dict_schema_version(state: Mapping[str, Any]) -> str:
    raise NotImplementedError


def validate_state_dict(state: Mapping[str, Any], schema_version: str) -> None:
    raise NotImplementedError
