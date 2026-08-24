# evaluation

Evaluation is independent of training loops and serving APIs. A suite defines
immutable dataset references, input transformation, model/inference contract,
metrics, aggregation, uncertainty/statistical method, pass/fail thresholds,
report schema, reproducibility settings, and safety policy.

- Owner: ml-evaluation
- Suite classes: sequence, structure, complexes, design, confidence
  calibration, robustness, and safety (plus regression and runtime
  performance harnesses).
- Every model release references an immutable evaluation report digest;
  dashboard state is never the release evidence.
- Numerical baselines record input generation and seed, exact package and
  toolchain versions, hardware class, precision mode, tolerance rationale,
  expected distribution, owner, and review date. A golden is never updated
  merely because a test failed.
- May depend on models, inference, data contracts, and metrics libraries;
  production model code must not depend on evaluation suites.
