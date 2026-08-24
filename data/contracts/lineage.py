from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LineageRecord:
    code_revision: str
    config_digest: str
    input_digests: tuple[str, ...]
    output_digests: tuple[str, ...]
    schema_version: str
    toolchain_identity: str
    validation_report_digest: str | None
    classification: str
    created_at: str
    actor: str
    idempotency_key: str
