# libs/python

Horizontal Python foundations used by tools, services, data workflows, and
local utilities: artifact references, configuration, contracts, identifiers,
observability, retry, serialization, testing helpers, and time.

- Owner: ml-platform
- Hard policy: this package must not depend on `torch`, model packages,
  training packages, CUDA-specific wheels, or GPU runtime initialization.
  PyTorch belongs in `models/`, `training/`, `evaluation/`, `inference/`, and
  GPU worker release units. `dependency_policy_test.py` enforces this.
- Packaged with `src/`-compatible layout as packaging boundaries are
  introduced; imports must work from an installed wheel and from Bazel.
- Test: `python3 -m unittest libs/python/dependency_policy_test.py` (plus
  Bazel targets as they land).
