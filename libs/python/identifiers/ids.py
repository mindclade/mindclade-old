from __future__ import annotations

import re
import uuid

KINDS = {
    "tenant": "tn",
    "project": "pj",
    "dataset": "ds",
    "artifact": "art",
    "job": "job",
    "experiment": "exp",
    "model": "mdl",
    "checkpoint": "ckpt",
}
_PREFIX_TO_KIND = {prefix: kind for kind, prefix in KINDS.items()}
_PATTERN = re.compile(r"^([a-z]{2,4})_([0-9a-f]{32})$")


def new_id(kind: str) -> str:
    if kind not in KINDS:
        raise ValueError(f"unknown identifier kind: {kind!r}")
    return f"{KINDS[kind]}_{uuid.uuid4().hex}"


def parse_id(value: str) -> tuple[str, str]:
    match = _PATTERN.fullmatch(value)
    if not match or match.group(1) not in _PREFIX_TO_KIND:
        raise ValueError(f"malformed identifier: {value!r}")
    return _PREFIX_TO_KIND[match.group(1)], match.group(2)


def is_valid(value: str) -> bool:
    try:
        parse_id(value)
    except ValueError:
        return False
    return True
