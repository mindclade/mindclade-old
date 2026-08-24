# runtime

Execution substrate shared by training and inference: distributed mesh,
collectives, topology, rendezvous and health; dispatch; memory; precision;
compilation; deterministic RNG streams; native extensions (Rust/CUDA/Python
adapters); diagnostics; and testing utilities.

- Owner: ml-runtime
- May depend on `libs/` and `protocols/`; must not contain model-specific
  policy.
- Unsupported execution paths fail explicitly; no silent fallbacks.
