from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SnapshotRef:
    source: str
    snapshot_id: str
    schema_version: str
    digest_algorithm: str
    digest: str
    size_bytes: int


@dataclass(frozen=True)
class Snapshot:
    ref: SnapshotRef
    input_digests: tuple[str, ...]
    created_at: str
    actor: str
