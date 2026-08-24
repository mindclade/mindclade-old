from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DispatchRecord:
    signature_key: str
    selected_implementation: str
    fallback_used: bool


@dataclass(frozen=True)
class QualificationResult:
    signature_key: str
    forward_parity: bool
    gradient_parity: bool
    determinism: bool | None
    performance_floor_met: bool
    report_digest: str
