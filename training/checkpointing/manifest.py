from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ShardEntry:
    path: str
    digest: str
    size_bytes: int


@dataclass(frozen=True)
class CheckpointManifest:
    schema_version: str
    step: int
    tokens_seen: int
    examples_seen: int
    topology: str
    parallel_plan_digest: str
    code_revision: str
    config_digest: str
    parent_checkpoint: str | None
    shards: tuple[ShardEntry, ...]
