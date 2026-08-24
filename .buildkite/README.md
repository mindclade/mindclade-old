# Buildkite pipelines

Buildkite is authoritative for affected-target planning, CPU builds and tests,
GPU tests and kernel qualification, distributed smoke tests, large integration
suites, nightly validation, clean-checkout release qualification, artifact
publication, and provenance/SBOM/signing.

`pipeline.yml` is the static entrypoint; `pipeline.py` generates the dynamic
pipeline from changed files, the reverse dependency graph, `component.yaml`
metadata, trust context, target tags, and release intent. The generated
pipeline is persisted as a build artifact so every build can be audited.

Untrusted pull-request builds receive no production secrets, cannot write
shared release caches, cannot publish artifacts, and run on isolated workers
with restricted network access. Trusted protected-branch and release builds
use OIDC workload identity rather than long-lived cloud keys.

Standard test tags: small, medium, large, network, integration, gpu, gpu-h100,
gpu-h200, gpu-b200, distributed, exclusive, flaky-quarantine, numerical,
kernel, performance, release.
