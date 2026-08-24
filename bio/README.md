# bio

Canonical biological domain: explicit, versioned semantics for atoms,
residues, chains, assemblies, sequences, alignments, chemical components,
missingness/uncertainty, alternate locations, provenance, and model-ready
features. The canonical semantic schema lives in `bio/schemas/`; Rust and
Python implementations must pass the same conformance fixtures.

- Owner: comp-bio
- Rust owns parsing and I/O for FASTA, A3M, Stockholm, mmCIF, PDB, CCD, and
  SDF (`formats/rust/`): streaming and bounded memory where practical, strict
  and permissive modes, structured diagnostics, byte offsets, deterministic
  output, fuzz and property tests, golden fixtures.
- Parsing answers "what does the source file contain"; scientific
  normalization ("what does this record mean for the model/dataset contract")
  stays above parsing and never merges with it. Source-faithful parsed
  records remain available for audit and reprocessing.
- Python bindings (`bindings/`) expose typed batches or Arrow-compatible
  structures without leaking Rust internals into model code.
- May depend on `libs/` and `protocols/`; never on data pipelines, models,
  training, services, workers, SDKs, or apps.
