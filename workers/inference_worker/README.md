# inference-worker

Python GPU worker for asynchronous inference jobs: queue/lease integration,
GPU process lifecycle, model bundle acquisition, invoking `inference/`,
heartbeats and cancellation, artifact upload, and operational telemetry.

- Owner: ml-inference
- Serving semantics live in `inference/`; network edge lives in
  `services/runtime_gateway`.
