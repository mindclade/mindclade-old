# kernels

Qualified accelerator kernels (TileLang, CUDA, bounded C++). Every optimized
operation ships a reference implementation, capability declaration, explicit
dispatch policy, autotuning search space, correctness/gradient/determinism
tests, hardware qualification, benchmarks, and a fallback policy.

- Owner: ml-performance
- Qualification keys include operation, implementation version, dtypes,
  accumulation dtype, shape family, layout/strides, mask/bias mode, device
  architecture, compiler/toolchain version, determinism mode, and tolerance
  profile. A benchmark result without this key is not actionable.
- Dispatch is explicit: resolve signature, select only qualified
  implementations for the current signature and hardware, apply policy
  constraints, record the selection in diagnostics, then fail clearly or use
  an explicitly approved reference fallback. Never a silent slower or
  numerically different path in a production qualification run.
- Benchmarks are structured artifacts compared statistically; a single best
  timing is not a release gate.
- May depend on `runtime/` and narrow foundational utilities; never training
  loops or service code.
