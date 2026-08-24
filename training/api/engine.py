from __future__ import annotations

from typing import Protocol


class TrainingEngine(Protocol):
    def initialize(
        self,
        task: TrainingTask,
        recipe: TrainingRecipe,
        topology: Topology,
    ) -> EngineState: ...

    def run(self, state: EngineState) -> TrainingResult: ...


class ParallelPlan(Protocol):
    def validate(self, model, topology, hardware) -> ValidationReport: ...
    def apply(self, model, mesh) -> ParallelizedModel: ...
