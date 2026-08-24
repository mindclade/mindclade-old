# bio/entities

Canonical biological entity implementations in Rust and Python over the
schemas in `bio/schemas/`. Both implementations must pass the shared
conformance fixtures in `conformance/`; divergence is a release blocker.

- Owner: comp-bio
- Scope: atoms, residues, polymer and non-polymer chains, assemblies,
  sequences and alphabets, chemical components and bonds, missingness,
  alternate locations and occupancy, provenance identifiers.
- Non-goals: parsing (see `bio/formats/`), featurization (see
  `bio/featurization/`), dataset policy (see `data/`).
