from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class KernelSignature:
    operation: str
    implementation_version: str
    input_dtypes: tuple[str, ...]
    output_dtypes: tuple[str, ...]
    accumulation_dtype: str
    shape_family: str
    layout: str
    mask_mode: str | None
    device_architecture: str
    toolchain_version: str
    determinism_mode: str
    tolerance_profile: str
