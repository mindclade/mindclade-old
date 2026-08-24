from __future__ import annotations

from typing import Protocol


class LoadPlanner(Protocol):
    def plan(self, manifest, topology): ...
