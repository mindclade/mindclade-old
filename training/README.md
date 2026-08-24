# training

Mindclade owns the trainer contract, training state, topology policy,
sharding plans, checkpoint schema, data semantics, and numerical
qualification; execution engines consume these contracts. Model code
describes mathematical structure; a separate parallel plan describes how it
is partitioned (model + task + topology + precision + plan = executable
distributed program), validated before launch.

- Owner: ml-training
- Primary production engine: native PyTorch distributed primitives with a
  TorchTitan-aligned engine (`engines/native`, `engines/titan`). Secondary:
  Lightning Fabric for single-node ergonomics (`engines/fabric`), never a
  second distributed control plane. Optional providers live behind narrow
  adapters.
- Checkpointing is a subsystem (`checkpointing/`): async save with bounded
  staging memory, atomic publication with completion markers, save/load
  planners, load-time resharding, partial load, format migration, corruption
  detection, retention, resume validation, and conversion to release bundles.
- Recipes (`recipes/`) are typed, validated, versioned configurations
  referencing immutable model config, dataset/feature versions, objective,
  optimizer/schedule, precision, parallel plan, checkpoint policy, evaluation
  suite, and resource profile. Secrets and cluster names are injected by the
  execution environment, never embedded.
- May depend on models, data, evaluation contracts, runtime, and kernels.
