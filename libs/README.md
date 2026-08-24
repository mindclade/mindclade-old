# libs

Genuinely horizontal, dependency-light foundations, one lane per language.
Domain logic (biological entities, parsing, feature schemas, model components,
dataset logic) belongs in domain packages, never here. `common`/`utils` grab
bags are rejected in review.

- Owner: per-lane (see CODEOWNERS)
- Dependency law: `libs/` may depend on `protocols/` and lower-level libraries
  in the same language, never on domain packages, services, or workers.
- Hard policy: `libs/python` is torch-free (no torch, model, training, or
  CUDA dependencies) — enforced by `libs/python/dependency_policy_test.py`.
