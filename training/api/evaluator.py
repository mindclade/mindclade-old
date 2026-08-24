from __future__ import annotations

from typing import Protocol


class Evaluator(Protocol):
    name: str

    def evaluate(self, model, state) -> dict: ...
