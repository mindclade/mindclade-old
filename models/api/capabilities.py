from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ModelCapabilities:
    tasks: tuple[str, ...]
    feature_schema_versions: tuple[str, ...]
    precisions: tuple[str, ...]
    supports_diffusion_sampling: bool
    supports_confidence: bool
