# training-worker

Python GPU worker executing training jobs: lease handling, topology
rendezvous, invoking `training/` engines against typed recipes, heartbeats,
cancellation, checkpoint upload, and structured training telemetry.

- Owner: ml-training
- Thin orchestration only; trainer contracts and checkpointing live in
  `training/`.
