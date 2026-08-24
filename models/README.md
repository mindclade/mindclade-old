# models

Model packages are pure execution units: typed configuration, module graph,
forward contracts, initialization, state-dict schema, checkpoint conversion,
supported tasks, feature requirements, output semantics, reference tests,
numerical qualification, and model card metadata. They own no cluster launch,
experiment database writes, queue consumption, HTTP handlers, or
environment-specific credentials.

- Owner: ml-research
- `components/` holds reusable pieces only after at least two real model
  consumers exist; until then components stay inside their family.
  Kernel-backed components retain a correct framework reference path.
- Released model bundles reference immutable weight shards, typed config,
  family/version, checkpoint schema version, feature schema requirements,
  tokenizer/vocabulary/chemical component versions, precision and hardware
  compatibility, qualified kernel signatures, code revision and provenance,
  evaluation report digest, safety metadata, license policy, and a model
  card. Serving never infers these from filenames.
- May depend on `bio/`, `kernels/`, `runtime/`, selected `libs/`; never
  training engines, network services, SDKs, or apps.
