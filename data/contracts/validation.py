from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class ValidationFinding:
    check: str
    severity: str
    message: str
    record_locator: str | None


@dataclass(frozen=True)
class ValidationReport:
    subject_digest: str
    passed: bool
    findings: tuple[ValidationFinding, ...]


class Validator(Protocol):
    def validate(self, subject_digest: str) -> ValidationReport: ...
