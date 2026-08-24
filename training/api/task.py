from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Protocol


class TrainingTask(Protocol):
    def build_model(self, context: ModelBuildContext) -> Model: ...
    def build_data(self, context: DataBuildContext) -> DataSource: ...
    def compute_loss(
        self,
        model: Model,
        batch: Batch,
        context: StepContext,
    ) -> LossOutput: ...
    def evaluators(self) -> Sequence[Evaluator]: ...
    def checkpointables(self) -> Mapping[str, Checkpointable]: ...
