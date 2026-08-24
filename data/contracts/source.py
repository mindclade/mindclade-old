from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SourceDescriptor:
    name: str
    uri: str
    revision: str | None
    license: str
    terms_url: str | None
    classification: str
