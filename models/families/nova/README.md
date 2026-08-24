# nova

First Mindclade model family. Owns its typed configuration, architecture,
tasks, checkpoint schema and conversion, inference adapters, qualification
suite, and tests. Components graduate to `models/components/` only once a
second family consumes them.

- Owner: ml-research
- Maturity: experimental
- Depends on `models/api`, `bio/`, `kernels/`, `runtime/`; never on training
  engines, services, SDKs, or apps.
