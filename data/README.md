# data

The data platform: immutable pipeline stages from source descriptor to model
feature dataset (raw object -> parsed batch -> normalized snapshot -> curated
dataset -> deduplicated/leakage-audited dataset -> split -> features). Every
stage transition is a versioned transformation carrying code revision, config
digest, input/output digest sets, schema version, toolchain identity,
validation report, policy classification, timestamps/actor, and an
idempotency key. Published dataset versions are never mutated.

- Owner: data-platform
- Connectors (PDB, UniProt, RNACentral, CCD) are adapters implementing one
  lifecycle: discover -> plan -> fetch -> verify -> parse -> normalize ->
  publish, with resumable downloads, rate limits, checksums, deterministic
  naming, idempotent replay, tombstones, and offline fixture mode for CI.
- Storage split: object storage for large artifacts, relational metadata for
  catalog/lineage/policy, a queue for execution, cache only for
  reconstructible acceleration. Weights and datasets never live in the
  relational database.
- Training-eligible datasets require schema and integrity validation,
  biological invariants, dedup and leakage reports, license/terms records,
  policy classification, split manifest, feature compatibility declaration,
  reproducibility record, and a dataset card.
- May depend on `bio/`, `libs/`, `protocols/`; model implementations only
  through the named featurization contract.
