# feature-worker

Rust and Python worker producing model feature datasets from curated
snapshots: featurization hot paths in Rust, feature semantics in Python,
with Python/Rust parity enforced by `bio/featurization/parity`.

- Owner: data-platform
- Outputs are immutable feature datasets with schema versions and lineage.
