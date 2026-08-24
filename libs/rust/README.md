# libs/rust

Horizontal Rust foundations: artifact references, byte utilities,
configuration, error taxonomy, identifiers, observability, retry, storage
access, and testing helpers.

- Owner: data-plane
- Crates stay cohesive (no one-crate-per-file); shared versions, metadata,
  and lints inherit from the workspace root `Cargo.toml`.
- Unsafe code lives behind narrow modules with explicit invariants and tests.
- Python bindings elsewhere are adapters over these stable Rust libraries,
  never the canonical implementation.
- May depend on `protocols/`; never on domain packages, services, or workers.
