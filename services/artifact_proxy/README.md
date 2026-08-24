# artifact-proxy

Rust service for high-throughput artifact transfer: content-addressed
streaming between clients, workers, and object storage with digest
verification, least-privilege scoping, and audit receipts.

- Owner: data-plane
- Never constructs object-store paths outside the artifact library contract;
  logical aliases resolve to immutable digests before execution.
