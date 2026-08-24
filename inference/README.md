# inference

Pure model execution, separate from network serving. Owns
request-to-feature conversion, bucketing and batching policy, model
execution, diffusion/sample orchestration, confidence computation, ranking,
postprocessing, artifact production, and execution diagnostics.

- Owner: ml-inference
- Network concerns live elsewhere: `services/runtime_gateway` owns authn/z,
  validation, tenancy/quotas, durable job creation, streaming/status,
  routing, and public error mapping; `workers/inference_worker` owns
  queue/lease integration, GPU process lifecycle, bundle acquisition,
  invoking this package, heartbeats/cancellation, artifact upload, and
  operational telemetry.
- Large results are artifact references, never embedded database rows or
  queue messages.
- May depend on models, runtime, kernels, and a minimal set of
  data/postprocessing contracts.
