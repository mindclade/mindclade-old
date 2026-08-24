# Mindclade Polyglot Monorepo Blueprint

**Status:** Proposed production baseline  
**Scope:** Mindclade internal product, platform, data, model, training, evaluation, inference, and developer tooling source  
**Audience:** Founding engineers, ML researchers, computational biologists, platform engineers, security, and technical leadership  
**Date:** 2026-08-23

---

## 1. Executive decision

Mindclade should use a **domain-first polyglot monorepo** with strong language lanes:

- **Python** owns model architecture, training, evaluation, inference semantics, scientific feature logic, and experimentation that has graduated into production.
- **Rust** owns high-throughput biological parsing, data-plane I/O, preprocessing hot paths, artifact transfer, CPU runtime components, and carefully bounded Python extensions.
- **Go** owns the control plane, durable job APIs, Kubernetes controllers, service infrastructure, authorization middleware, and operational automation.
- **TypeScript** owns the web console, administrative surfaces, documentation application, and browser/server SDKs.
- **Protobuf and JSON Schema** own stable cross-process and cross-language contracts.
- **TileLang, CUDA, and limited C++** form a specialized accelerator lane for qualified kernels and native extensions.
- **Bazel/Starlark, Nix, and shell** are build and developer-environment tools, not places for product logic.

The monorepo is the authoritative source for application code and service-owned deployment packages. It does **not** own organization governance, foundational cloud trust, live cloud desired state, or live Kubernetes environment promotion. Those remain in separate repositories.

The default application architecture is a **Go modular control-plane monolith plus specialized Rust and Python workers**, not a fleet of premature microservices.

Bazel is the repository-wide integration graph. Native ecosystem managers remain the source of truth for ecosystem dependency resolution and local developer ergonomics:

- `uv` for Python
- Cargo for Rust
- one root Go module for internal Go code
- `pnpm` for TypeScript
- Buf for Protobuf
- Nix for pinned developer tools and system libraries

There is no repository-wide release version. Services, SDKs, schemas, models, datasets, kernels, and deployment packages are versioned according to their own artifact semantics.

---

## 2. Goals

The monorepo must make these outcomes routine:

1. A model change can atomically update its kernels, feature schemas, training recipe, evaluation suite, serving path, and SDK contract.
2. A clean checkout can build, test, qualify, and package every releasable target without depending on an engineer's workstation state.
3. Every dataset, feature set, checkpoint, model bundle, kernel binary, image, and SDK can be traced to source revision, inputs, build identity, schema, and policy.
4. CPU-only contributors can work productively without installing the full GPU stack.
5. GPU workflows can be reproduced across local development, CI, and cluster execution.
6. Cross-language interactions are explicit, versioned, and testable.
7. Research code has a clear graduation path into supported production packages.
8. Biological data and model artifacts are governed as first-class security assets.
9. CI scales by affected targets rather than running the entire repository for every change.
10. The repository can support frontier model research without allowing research urgency to erode platform correctness.

### Non-goals

This blueprint does not attempt to:

- turn every domain module into a network service;
- force every language dependency through Bazel alone;
- treat notebooks as production entrypoints;
- store large datasets, model weights, generated experiment output, or secrets in Git;
- put production environment overlays or cloud credentials in the source monorepo;
- create a custom orchestrator, scheduler, feature store, service mesh, or package registry before one is justified;
- make Python a control-plane language or Go a model-numerics language;
- hide unsupported execution behind silent fallbacks.

---

## 3. Repository estate and trust boundaries

```text
.github
    |
    | shared organization templates and reusable GitHub workflows
    v
github-config
    |
    | GitHub Enterprise policy, teams, rulesets, repository settings,
    | environments, Actions/OIDC governance
    v
+----------------------+----------------------+----------------------+
| bootstrap            | infrastructure-live  | gitops               |
|                      |                      |                      |
| durable identity,    | normal cloud desired| Kubernetes desired   |
| state, recovery,     | state and shared    | state, Argo CD apps, |
| break-glass trust    | infrastructure      | environment promotion|
+----------------------+----------------------+----------------------+
                                  ^
                                  |
                      immutable artifact digests
                                  |
                                  v
                      mindclade internal monorepo
```

### Repository ownership

| Repository | Owns | Must not own |
|---|---|---|
| `.github` | Organization profile, community health files, shared workflow implementations and templates | Product code, cloud state, environment credentials |
| `github-config` | Organization/repository governance, teams, rulesets, Actions policy, OIDC policy | Runtime services or Kubernetes application manifests |
| `bootstrap` | Minimum durable cloud trust, state, recovery, break-glass IAM | Normal application infrastructure |
| `infrastructure-live` | Cloud projects/accounts, networks, clusters, storage, databases, registries, observability backends | Application source or model code |
| `gitops` | Environment-specific Kubernetes desired state and promotion by immutable digest | Building application artifacts |
| `mindclade` | Product, model, data, training, evaluation, inference, service, worker, SDK, and service-owned deployment source | Live cloud/environment desired state |
| Public SDK repositories | Stable public SDKs only when external distribution requires independent lifecycle and visibility | Internal implementation details |

### Monorepo deployment boundary

The monorepo may contain:

- service-owned Helm charts or Kustomize bases;
- CRDs and generated CRD documentation;
- local and integration-test deployment definitions;
- policy tests;
- container build definitions;
- canonical default configuration.

The monorepo must not contain:

- production cluster names or credentials;
- production secret references tied to a specific environment;
- mutable image tags used for production;
- environment promotion state;
- Terraform root modules for live environments.

The `gitops` repository consumes versioned deployment packages and immutable image digests produced by the monorepo.

---

## 4. Language ownership model

| Lane | Primary ownership | Allowed secondary use | Explicit exclusions |
|---|---|---|---|
| Python | Model definitions, objectives, training, evaluation, inference pipelines, scientific transformations, feature semantics | Thin orchestration inside GPU workers; bindings over Rust/native extensions | Control-plane services, high-volume parsers when Rust is justified, cloud controllers, generic platform daemons |
| Rust | Biological format parsing, high-throughput I/O, normalization hot paths, artifact streaming, CPU runtime, memory-safe native extensions | Selected low-latency services and command-line tools | Model research framework, business workflow orchestration, web product |
| Go | Control plane, APIs, Kubernetes controllers, durable job lifecycle, authorization, tenancy, operational services | CLIs and release automation | Tensor numerics, scientific feature semantics, GPU kernels |
| TypeScript | Console, admin, docs app, web/server SDKs, design system | Repository developer tools where Node is already required | Model execution and cluster control plane |
| Protobuf / JSON Schema | RPC, events, manifests, compatibility contracts | Generated OpenAPI and SDK models | Business logic |
| TileLang / CUDA / C++ | Performance-critical GPU kernels and native operators | Narrow native interfaces | General application logic |
| Starlark / Nix / shell | Hermetic build graph, toolchain pinning, bootstrap, small wrappers | Repository automation | Domain or product behavior |

### Hard policy: `libs/python` is torch-free

`libs/python` is a horizontal foundation used by tools, services, data workflows, and local utilities. It must not depend on:

- `torch`;
- model packages;
- training packages;
- CUDA-specific wheels;
- GPU runtime initialization.

PyTorch belongs in `models/`, `training/`, `evaluation/`, `inference/`, and GPU worker release units. A dependency-policy test must enforce this rule.

---

## 5. Organizing principle: domain first, language second

Top-level directories represent durable business or technical domains. Language-specific implementations live inside those domains where needed.

Prefer:

```text
data/ingestion/pdb/rust/
models/families/nova/python/
services/control_plane/go/
```

over:

```text
python/everything/
rust/everything/
go/everything/
```

A language-first repository becomes four adjacent repositories with weak integration. A domain-first repository keeps each capability's contracts, tests, documentation, and implementations close together while retaining language boundaries.

`libs/` is reserved for genuinely horizontal capabilities. Biological entities, mmCIF parsing, feature schemas, model components, and dataset logic are domain packages, not generic libraries.

---

## 6. Proposed source tree

The tree below is the target architecture. Create a directory only when it has an owner and at least one real target; the tree is a boundary map, not permission to fill the repository with empty stubs.

```text
mindclade/
├── .buildkite/
│   ├── pipeline.yml
│   ├── pipeline.py
│   ├── hooks/
│   │   ├── environment
│   │   └── pre-command
│   ├── lib/
│   │   ├── affected_targets.py
│   │   ├── annotations.py
│   │   ├── pipeline_model.py
│   │   └── trusted_context.py
│   ├── steps/
│   │   ├── presubmit.py
│   │   ├── gpu.py
│   │   ├── nightly.py
│   │   ├── release.py
│   │   └── security.py
│   └── README.md
├── .github/
│   ├── actions/
│   │   ├── setup-repository/
│   │   └── validate-metadata/
│   ├── workflows/
│   │   ├── pr-metadata.yml
│   │   ├── lightweight-presubmit.yml
│   │   ├── required-check.yml
│   │   ├── docs.yml
│   │   ├── dependency-review.yml
│   │   └── mirror-verification.yml
│   ├── CODEOWNERS
│   ├── dependabot.yml
│   └── pull_request_template.md
├── .devcontainer/
├── .vscode/
├── MODULE.bazel
├── BUILD.bazel
├── .bazelrc
├── .bazelversion
├── flake.nix
├── flake.lock
├── pyproject.toml
├── uv.lock
├── .python-version
├── Cargo.toml
├── Cargo.lock
├── rust-toolchain.toml
├── go.mod
├── go.sum
├── package.json
├── pnpm-workspace.yaml
├── pnpm-lock.yaml
├── buf.yaml
├── buf.gen.yaml
├── justfile
├── .editorconfig
├── .gitattributes
├── .gitignore
├── .pre-commit-config.yaml
├── CONTRIBUTING.md
├── SECURITY.md
├── CODE_OF_CONDUCT.md
├── LICENSE
├── NOTICE
├── README.md
│
├── protocols/
│   ├── proto/
│   │   └── mindclade/
│   │       ├── common/v1/
│   │       ├── artifact/v1/
│   │       ├── dataset/v1/
│   │       ├── experiment/v1/
│   │       ├── model/v1/
│   │       ├── training/v1/
│   │       ├── inference/v1/
│   │       ├── evaluation/v1/
│   │       ├── policy/v1/
│   │       └── admin/v1/
│   ├── events/
│   │   └── mindclade/
│   │       ├── artifact/v1/
│   │       ├── job/v1/
│   │       ├── model/v1/
│   │       └── audit/v1/
│   ├── schemas/
│   │   ├── artifact_manifest/
│   │   ├── dataset_manifest/
│   │   ├── feature_manifest/
│   │   ├── checkpoint_manifest/
│   │   ├── model_manifest/
│   │   └── kernel_qualification/
│   ├── openapi/
│   ├── generated/
│   │   ├── go/
│   │   ├── python/
│   │   ├── rust/
│   │   └── typescript/
│   ├── compatibility/
│   │   ├── baselines/
│   │   └── tests/
│   ├── BUILD.bazel
│   └── README.md
│
├── libs/
│   ├── python/
│   │   ├── artifacts/
│   │   ├── config/
│   │   ├── contracts/
│   │   ├── identifiers/
│   │   ├── observability/
│   │   ├── retry/
│   │   ├── serialization/
│   │   ├── testing/
│   │   ├── time/
│   │   ├── dependency_policy_test.py
│   │   ├── BUILD.bazel
│   │   └── README.md
│   ├── rust/
│   │   ├── artifact/
│   │   ├── bytes/
│   │   ├── config/
│   │   ├── errors/
│   │   ├── identifiers/
│   │   ├── observability/
│   │   ├── retry/
│   │   ├── storage/
│   │   ├── testing/
│   │   └── README.md
│   ├── go/
│   │   ├── audit/
│   │   ├── auth/
│   │   ├── clock/
│   │   ├── connectx/
│   │   ├── controller/
│   │   ├── faults/
│   │   ├── grpcx/
│   │   ├── identifiers/
│   │   ├── kubernetes/
│   │   ├── middleware/
│   │   ├── observability/
│   │   ├── servicekit/
│   │   ├── storage/
│   │   ├── testing/
│   │   └── README.md
│   ├── typescript/
│   │   ├── config/
│   │   ├── design_system/
│   │   ├── observability/
│   │   ├── testing/
│   │   ├── web/
│   │   └── README.md
│   ├── BUILD.bazel
│   └── README.md
│
├── bio/
│   ├── schemas/
│   │   ├── atom/
│   │   ├── residue/
│   │   ├── chain/
│   │   ├── assembly/
│   │   ├── sequence/
│   │   └── feature/
│   ├── entities/
│   │   ├── rust/
│   │   ├── python/
│   │   ├── conformance/
│   │   └── README.md
│   ├── formats/
│   │   ├── rust/
│   │   │   ├── fasta/
│   │   │   ├── a3m/
│   │   │   ├── stockholm/
│   │   │   ├── mmcif/
│   │   │   ├── pdb/
│   │   │   ├── ccd/
│   │   │   └── sdf/
│   │   ├── python/
│   │   ├── fixtures/
│   │   └── conformance/
│   ├── chemistry/
│   │   ├── python/
│   │   └── tests/
│   ├── sequences/
│   │   ├── python/
│   │   └── tests/
│   ├── structures/
│   │   ├── python/
│   │   └── tests/
│   ├── alignments/
│   │   ├── python/
│   │   ├── rust/
│   │   └── tests/
│   ├── featurization/
│   │   ├── python/
│   │   ├── rust/
│   │   ├── schemas/
│   │   ├── parity/
│   │   └── tests/
│   ├── bindings/
│   │   ├── python/
│   │   └── abi/
│   ├── BUILD.bazel
│   └── README.md
│
├── data/
│   ├── contracts/
│   │   ├── source.py
│   │   ├── snapshot.py
│   │   ├── lineage.py
│   │   ├── validation.py
│   │   └── BUILD.bazel
│   ├── connectors/
│   │   ├── api/
│   │   ├── pdb/
│   │   ├── uniprot/
│   │   ├── rnacentral/
│   │   ├── ccd/
│   │   └── tests/
│   ├── ingestion/
│   │   ├── fetch/
│   │   ├── resume/
│   │   ├── manifests/
│   │   ├── rate_limits/
│   │   ├── integrity/
│   │   └── tests/
│   ├── normalization/
│   ├── curation/
│   ├── validation/
│   │   ├── schema/
│   │   ├── biological/
│   │   ├── policy/
│   │   └── quality/
│   ├── deduplication/
│   ├── leakage/
│   ├── splits/
│   ├── sampling/
│   ├── featurization/
│   ├── catalog/
│   ├── storage/
│   ├── fixtures/
│   ├── tools/
│   ├── BUILD.bazel
│   └── README.md
│
├── kernels/
│   ├── api/
│   │   ├── operation.py
│   │   ├── signature.py
│   │   ├── capability.py
│   │   └── result.py
│   ├── common/
│   │   ├── layouts/
│   │   ├── numerics/
│   │   ├── tma/
│   │   ├── swizzle/
│   │   └── utilities/
│   ├── registry/
│   ├── dispatch/
│   ├── attention/
│   │   ├── reference.py
│   │   ├── tilelang.py
│   │   ├── dispatch.py
│   │   ├── autotune.py
│   │   ├── spec.py
│   │   ├── tests/
│   │   └── benchmarks/
│   ├── pairformer/
│   │   ├── triangle_attention/
│   │   ├── triangle_multiplication/
│   │   ├── outer_product_mean/
│   │   ├── transition/
│   │   ├── tests/
│   │   └── benchmarks/
│   ├── diffusion/
│   ├── moe/
│   ├── normalization/
│   ├── quantization/
│   ├── qualification/
│   │   ├── correctness/
│   │   ├── gradients/
│   │   ├── determinism/
│   │   ├── performance/
│   │   ├── hardware/
│   │   └── reports/
│   ├── benchmarks/
│   ├── tests/
│   ├── BUILD.bazel
│   └── README.md
│
├── runtime/
│   ├── distributed/
│   │   ├── mesh/
│   │   ├── collectives/
│   │   ├── topology/
│   │   ├── rendezvous/
│   │   └── health/
│   ├── dispatch/
│   ├── memory/
│   ├── precision/
│   ├── compilation/
│   ├── rng/
│   ├── extensions/
│   │   ├── rust/
│   │   ├── cuda/
│   │   └── python/
│   ├── diagnostics/
│   ├── testing/
│   ├── BUILD.bazel
│   └── README.md
│
├── models/
│   ├── api/
│   │   ├── model.py
│   │   ├── batch.py
│   │   ├── outputs.py
│   │   ├── capabilities.py
│   │   └── serialization.py
│   ├── common/
│   │   ├── configuration/
│   │   ├── initialization/
│   │   ├── masking/
│   │   ├── embeddings/
│   │   └── losses/
│   ├── components/
│   │   ├── sequence/
│   │   ├── pairformer/
│   │   ├── diffusion/
│   │   ├── confidence/
│   │   ├── geometry/
│   │   ├── heads/
│   │   └── moe/
│   ├── families/
│   │   └── nova/
│   │       ├── configuration/
│   │       ├── architecture/
│   │       ├── tasks/
│   │       ├── checkpoints/
│   │       ├── conversion/
│   │       ├── inference/
│   │       ├── qualification/
│   │       ├── tests/
│   │       ├── BUILD.bazel
│   │       ├── component.yaml
│   │       └── README.md
│   ├── registry/
│   ├── packaging/
│   ├── conversion/
│   ├── tests/
│   ├── BUILD.bazel
│   └── README.md
│
├── training/
│   ├── api/
│   │   ├── task.py
│   │   ├── engine.py
│   │   ├── state.py
│   │   ├── optimizer.py
│   │   ├── evaluator.py
│   │   └── callbacks.py
│   ├── engines/
│   │   ├── native/
│   │   ├── titan/
│   │   ├── fabric/
│   │   └── single_process/
│   ├── state/
│   ├── parallel/
│   │   ├── planning/
│   │   ├── data/
│   │   ├── tensor/
│   │   ├── pipeline/
│   │   ├── context/
│   │   ├── expert/
│   │   └── validation/
│   ├── checkpointing/
│   │   ├── api.py
│   │   ├── manager.py
│   │   ├── schema.py
│   │   ├── manifest.py
│   │   ├── save_planner.py
│   │   ├── load_planner.py
│   │   ├── async_save.py
│   │   ├── atomic_commit.py
│   │   ├── reshard.py
│   │   ├── resume.py
│   │   ├── integrity.py
│   │   ├── retention.py
│   │   ├── conversion.py
│   │   ├── migration.py
│   │   └── tests/
│   ├── data/
│   ├── precision/
│   ├── optimization/
│   ├── schedules/
│   ├── objectives/
│   │   ├── sequence/
│   │   ├── structure/
│   │   ├── diffusion/
│   │   └── moe/
│   ├── loops/
│   ├── callbacks/
│   ├── launch/
│   ├── resilience/
│   ├── telemetry/
│   ├── recipes/
│   │   ├── smoke/
│   │   ├── pretraining/
│   │   ├── finetuning/
│   │   └── qualification/
│   ├── tests/
│   ├── BUILD.bazel
│   └── README.md
│
├── evaluation/
│   ├── api/
│   ├── harness/
│   ├── metrics/
│   ├── suites/
│   │   ├── sequence/
│   │   ├── structure/
│   │   ├── complexes/
│   │   ├── design/
│   │   ├── confidence/
│   │   ├── robustness/
│   │   └── safety/
│   ├── datasets/
│   ├── regression/
│   ├── reports/
│   ├── fixtures/
│   ├── tests/
│   ├── BUILD.bazel
│   └── README.md
│
├── inference/
│   ├── api/
│   ├── pipeline/
│   ├── batching/
│   ├── sampling/
│   ├── compilation/
│   ├── postprocessing/
│   ├── confidence/
│   ├── ranking/
│   ├── artifacts/
│   ├── diagnostics/
│   ├── tests/
│   ├── BUILD.bazel
│   └── README.md
│
├── services/
│   ├── control_plane/
│   │   ├── cmd/control-plane/
│   │   ├── internal/
│   │   │   ├── artifacts/
│   │   │   ├── datasets/
│   │   │   ├── experiments/
│   │   │   ├── jobs/
│   │   │   ├── models/
│   │   │   ├── policies/
│   │   │   ├── projects/
│   │   │   ├── tenants/
│   │   │   ├── users/
│   │   │   └── platform/
│   │   │       ├── database/
│   │   │       ├── outbox/
│   │   │       ├── queue/
│   │   │       └── storage/
│   │   ├── migrations/
│   │   ├── tests/
│   │   ├── BUILD.bazel
│   │   ├── component.yaml
│   │   └── README.md
│   ├── runtime_gateway/
│   │   ├── cmd/runtime-gateway/
│   │   ├── internal/
│   │   ├── tests/
│   │   ├── BUILD.bazel
│   │   ├── component.yaml
│   │   └── README.md
│   ├── artifact_proxy/
│   │   ├── src/
│   │   ├── tests/
│   │   ├── Cargo.toml
│   │   ├── BUILD.bazel
│   │   ├── component.yaml
│   │   └── README.md
│   ├── webhook_dispatcher/        # create when external webhooks are real
│   ├── event_dispatcher/          # split only after outbox volume justifies it
│   ├── BUILD.bazel
│   └── README.md
│
├── workers/
│   ├── ingestion_worker/
│   │   ├── rust/
│   │   ├── tests/
│   │   ├── BUILD.bazel
│   │   ├── component.yaml
│   │   └── README.md
│   ├── feature_worker/
│   │   ├── rust/
│   │   ├── python/
│   │   ├── tests/
│   │   ├── BUILD.bazel
│   │   ├── component.yaml
│   │   └── README.md
│   ├── training_worker/
│   │   ├── python/
│   │   ├── tests/
│   │   ├── BUILD.bazel
│   │   ├── component.yaml
│   │   └── README.md
│   ├── evaluation_worker/
│   │   ├── python/
│   │   ├── tests/
│   │   ├── BUILD.bazel
│   │   ├── component.yaml
│   │   └── README.md
│   ├── inference_worker/
│   │   ├── python/
│   │   ├── tests/
│   │   ├── BUILD.bazel
│   │   ├── component.yaml
│   │   └── README.md
│   ├── BUILD.bazel
│   └── README.md
│
├── sdk/
│   ├── python/
│   │   ├── src/mindclade/
│   │   ├── tests/
│   │   ├── pyproject.toml
│   │   ├── BUILD.bazel
│   │   └── README.md
│   ├── typescript/
│   │   ├── src/
│   │   ├── tests/
│   │   ├── package.json
│   │   ├── BUILD.bazel
│   │   └── README.md
│   ├── go/                        # reserve until external demand exists
│   ├── rust/                      # reserve until external demand exists
│   ├── conformance/
│   ├── examples/
│   ├── BUILD.bazel
│   └── README.md
│
├── apps/
│   ├── console/
│   │   ├── app/
│   │   ├── components/
│   │   ├── features/
│   │   ├── tests/
│   │   ├── package.json
│   │   ├── BUILD.bazel
│   │   ├── component.yaml
│   │   └── README.md
│   ├── admin/
│   ├── docs/
│   ├── BUILD.bazel
│   └── README.md
│
├── deploy/
│   ├── crds/
│   ├── components/
│   │   ├── control_plane/
│   │   ├── runtime_gateway/
│   │   ├── artifact_proxy/
│   │   └── workers/
│   ├── local/
│   ├── integration/
│   ├── policies/
│   ├── tests/
│   ├── BUILD.bazel
│   └── README.md
│
├── research/
│   ├── notebooks/
│   ├── prototypes/
│   ├── ablations/
│   ├── studies/
│   ├── papers/
│   ├── fixtures/
│   ├── README.md
│   └── POLICY.md
│
├── tests/
│   ├── conformance/
│   ├── integration/
│   ├── end_to_end/
│   ├── distributed/
│   ├── failure_injection/
│   ├── performance/
│   ├── security/
│   └── README.md
│
├── tools/
│   ├── bazel/
│   │   ├── rules/
│   │   ├── macros/
│   │   ├── aspects/
│   │   └── transitions/
│   ├── ci/
│   ├── codegen/
│   ├── dev/
│   ├── repo/
│   ├── release/
│   ├── qualification/
│   ├── migration/
│   ├── generators/
│   ├── licenses/
│   └── README.md
│
├── docs/
│   ├── architecture/
│   ├── adr/
│   ├── domains/
│   ├── standards/
│   ├── developer/
│   ├── security/
│   ├── runbooks/
│   ├── operations/
│   ├── model_cards/
│   ├── dataset_cards/
│   └── README.md
│
├── examples/
│   ├── sdk/
│   ├── data_connector/
│   ├── model_extension/
│   ├── training_smoke/
│   └── inference/
│
└── third_party/
    ├── patches/
    ├── licenses/
    ├── notices/
    ├── source_mirrors/
    ├── BUILD.bazel
    └── README.md
```

---

## 7. Dependency laws

These laws are more important than the visual tree.

### 7.1 Layered dependency direction

```text
protocols ------------------------------> sdk ----------------> apps
    |
    v
  libs
  /  \
 v    v
bio  runtime
 |      |
 v      v
data -> kernels
  \      /
   v    v
    models
   /   |   \
  v    v    v
training inference evaluation
  |       |       |
  v       v       v
training inference evaluation
 worker    worker    worker

data --------------------------> ingestion / feature workers
protocols + selected libs -----> control-plane and gateway services
```

Services and workers are composition roots. SDKs depend on public protocols, not on
service implementation packages.

The diagram is directional, not a claim that every node depends on every predecessor.

### 7.2 Import rules

1. `protocols/` may not depend on implementation packages.
2. `libs/` may depend on `protocols/` and other lower-level libraries within the same language, but never on domain packages.
3. `bio/` may depend on `libs/` and `protocols/`; it may not depend on data pipelines, models, training, services, workers, SDKs, or apps.
4. `data/` may depend on `bio/`, `libs/`, and `protocols/`; it may not depend on model implementations except through an explicitly named featurization contract.
5. `runtime/` may depend on `libs/` and `protocols/`; it may not contain model-specific policy.
6. `kernels/` may depend on `runtime/` and narrow foundational utilities; it may not import training loops or service code.
7. `models/` may depend on `bio/`, `kernels/`, `runtime/`, and selected `libs/`; it may not import training engines, network services, SDKs, or apps.
8. `training/` may depend on models, data, evaluation contracts, runtime, and kernels.
9. `evaluation/` may depend on models, inference, data contracts, and metrics libraries; production model code must not depend on evaluation suites.
10. `inference/` may depend on models, runtime, kernels, and a minimal set of data/postprocessing contracts.
11. `services/` and `workers/` are composition roots. No foundational or domain package may import from them.
12. `sdk/` consumes generated protocol clients and public hand-written convenience layers; it does not import service implementation code.
13. `apps/` consume SDKs and design-system packages only. They do not import generated database types, Go internals, or model code.
14. `research/` may import production code. Production code may never import from `research/`.
15. `deploy/` references packaged components and generated configuration schemas; application code must not parse live environment overlays from `deploy/`.

### 7.3 Cross-language boundaries

Allowed cross-language mechanisms:

- Protobuf RPC or messages;
- versioned event envelopes;
- JSON Schema manifests;
- Arrow-compatible columnar data or well-defined file formats;
- a narrow C ABI;
- PyO3/maturin-style Python extension modules;
- subprocess boundaries for deployable workers;
- content-addressed artifacts in object storage.

Disallowed mechanisms:

- copying business models independently into four languages;
- importing generated database structs as API contracts;
- Python shelling into Go or Rust libraries as an internal call mechanism;
- unversioned ad hoc JSON dictionaries crossing services;
- shared mutable files used as inter-process coordination;
- direct database access across service/module ownership boundaries.

### 7.4 Architecture enforcement

Enforce the laws with:

- Bazel visibility;
- Python import-linter or custom AST policy tests;
- Rust workspace dependency policy;
- Go `internal/` packages and static checks;
- TypeScript project references and package exports;
- CODEOWNERS;
- a repository dependency graph check in presubmit.

Exceptions require an ADR with an owner and removal condition.

---

## 8. Standard package shape

Every maintained package should provide the same minimum evidence.

```text
package/
├── README.md
├── BUILD.bazel
├── component.yaml          # for releasable/deployable/operational components
├── src/ or language-native source layout
├── tests/
└── fixtures/               # only when owned by the package
```

### README requirements

A package README states:

- purpose and non-goals;
- owner;
- public entrypoints;
- dependency restrictions;
- data classifications handled;
- build and test commands;
- compatibility contract;
- failure modes;
- operational considerations if deployable;
- graduation or deprecation status.

### `component.yaml`

Each deployable or independently releasable component has machine-readable metadata.

```yaml
apiVersion: mindclade.dev/v1
kind: Service
metadata:
  name: control-plane
  owner: platform-control-plane
spec:
  maturity: production
  tier: 1
  languages: [go]
  buildTargets:
    - //services/control_plane/cmd/control-plane
  testTargets:
    - //services/control_plane/...
  artifacts:
    - type: oci
      name: control-plane
  protocols:
    - mindclade.training.v1
    - mindclade.artifact.v1
  dataClassifications:
    - internal
    - confidential-metadata
  runtime:
    kubernetes: true
    gpu: false
```

Use this catalog to drive CI selection, ownership validation, deployment documentation, developer portal metadata, release manifests, and security review.

---

## 9. Build and dependency architecture

### 9.1 Bazel is the integration graph

Bazel owns:

- repository-wide target graph;
- source visibility and dependency enforcement;
- code generation;
- tests;
- binaries and OCI packaging;
- affected-target analysis;
- clean-checkout builds;
- remote cache and remote execution where appropriate;
- release target composition;
- build metadata and provenance inputs.

Use Bzlmod through `MODULE.bazel`. Do not introduce a legacy `WORKSPACE` dependency graph.

Bazel must not become a second handwritten dependency registry that drifts from native manifests. Repository rules and module extensions should consume or validate native lock state where practical.

### 9.2 Native ecosystem managers remain authoritative

| Ecosystem | Root policy |
|---|---|
| Python | One root `uv` workspace and lockfile; a small number of workspace members aligned to real packaging/environment boundaries |
| Rust | One root Cargo workspace and `Cargo.lock`; workspace-inherited metadata, lints, and dependencies |
| Go | One root `go.mod` for internal Go code; avoid a committed `go.work` unless Mindclade intentionally adopts multiple independently released modules |
| TypeScript | One `pnpm` workspace and lockfile; internal packages use `workspace:` references |
| Protobuf | One Buf workspace/configuration; lint and breaking checks required |
| Nix | One flake and lockfile for developer tools, native libraries, and reproducible shells |
| Bazel | One `MODULE.bazel` and pinned Bazel version |

### 9.3 Python environment policy

Use one lockfile, but expose named dependency groups and execution profiles:

- `dev`: formatting, linting, type checking, unit testing;
- `cpu`: CPU-only model smoke tests and data tools;
- `gpu`: PyTorch, CUDA-integrated packages, training and inference;
- `docs`: documentation build;
- `release`: wheel and package tooling.

Rules:

- workspace members are release or environment boundaries, not every directory;
- all production packages use `src/` layout when packaged as wheels;
- no editable-path behavior is required in CI;
- package imports must work from an installed wheel and from Bazel;
- GPU images consume a locked, exported dependency set;
- custom wheels are mirrored into a controlled package store;
- `libs/python` remains torch-free.

### 9.4 Rust workspace policy

- Put shared dependency versions, package metadata, and lints at workspace root.
- Keep crates cohesive; do not create one crate per source file.
- Prefer pure Rust APIs internally.
- Put unsafe code behind narrow modules with explicit invariants and tests.
- Treat Python bindings as adapters over stable Rust libraries, not the canonical implementation.
- Run `cargo check`, tests, clippy, formatting, dependency auditing, and Bazel parity checks.

### 9.5 Go module policy

Use one internal module at the repository root. Recommended import path:

```text
github.com/Mindclade/mindclade
```

This avoids a vanity-domain availability dependency for private internal builds. Public Go SDKs can later move to a dedicated public repository and a stable vanity import path if external distribution justifies it.

Rules:

- deployable binaries live under `cmd/`;
- non-public service code lives under service-local `internal/`;
- horizontal libraries live under `libs/go/`;
- do not create a `go.mod` in every library;
- service modules do not share database implementation packages;
- CI tests the repository without hidden local replacements.

### 9.6 TypeScript workspace policy

- Use scoped packages such as `@mindclade/sdk`, `@mindclade/design-system`, and `@mindclade/config`.
- Apps consume packages through declared exports, never relative paths escaping package roots.
- Generated protocol clients are wrapped by SDK layers rather than imported directly throughout UI features.
- Keep browser-safe packages separate from Node-only packages.
- Apply strict TypeScript settings and API-extractor-style public surface checks for released packages.

### 9.7 Nix responsibility

Nix pins:

- compiler and interpreter toolchains;
- Bazel, Buf, Node, pnpm, uv, Rust, Go, and native build utilities;
- system libraries needed by parsers and native extensions;
- consistent local shells for CPU, GPU-tooling, docs, and release work.

Nix does not replace `uv.lock`, `Cargo.lock`, `go.mod`, or `pnpm-lock.yaml`. It pins the tools that interpret them and the system-level dependencies they cannot express cleanly.

### 9.8 Command ergonomics

`justfile` is a discoverable command index, not a second build system.

Recommended commands:

```text
just bootstrap
just doctor
just format
just lint
just test
just test-affected
just build
just build-affected
just proto
just docs
just train-smoke
just inference-smoke
just kernel-qualify
just integration
just release-check
```

Each command delegates to Bazel or a native tool. Complex logic belongs in tested programs under `tools/`, not shell one-liners embedded in `justfile`.

---

## 10. Protocol and schema architecture

### 10.1 Source of truth

Use Protobuf as the source of truth for:

- internal RPC;
- durable job requests and status;
- service events;
- audit event payloads;
- generated client models.

Use JSON Schema for:

- artifact manifests;
- dataset, feature, checkpoint, and model manifests;
- human-authored configuration that must be validated outside a Protobuf runtime;
- policy documents where JSON/YAML interoperability matters.

Generate OpenAPI only for public HTTP edges. Do not make an OpenAPI document and Protobuf schema independently authoritative for the same API.

### 10.2 Versioning rules

- Stable packages use `v1`, `v2`, and so on.
- Experimental APIs use a clearly marked namespace and may not be consumed by stable SDKs.
- Never reuse a Protobuf field number.
- Reserve removed field names and numbers.
- Events are immutable after publication; new meaning requires a new field or version.
- Manifests include `schemaVersion`.
- CI compares protocol changes against the protected baseline.
- Breaking changes require an approved migration plan and coordinated SDK/service rollout.

### 10.3 Generated code policy

Generated files are never hand-edited.

Check generated code into Git only when one of these is true:

- an external SDK release requires it;
- consumers cannot run the generator;
- generated output is required for source distribution;
- reviewability materially improves safety.

Otherwise, generate hermetically in Bazel and release pipelines. A presubmit target must detect drift for any checked-in generated output.

---

## 11. Biological domain architecture

### 11.1 Canonical entity semantics

Mindclade needs explicit, versioned semantics for:

- atoms and coordinates;
- residues and modifications;
- polymer and non-polymer chains;
- assemblies and biological units;
- sequences and alphabets;
- alignments;
- chemical components and bonds;
- missingness and uncertainty;
- alternate locations and occupancy;
- provenance and source identifiers;
- model-ready features.

The canonical semantic schema lives under `bio/schemas/`. Rust and Python implementations must pass the same conformance fixtures.

### 11.2 Parsing and I/O

Rust is the default for:

- FASTA;
- A3M;
- Stockholm;
- mmCIF;
- PDB;
- CCD;
- SDF or equivalent small-molecule exchange formats;
- compressed stream handling;
- indexing and random access;
- validation over large corpora.

A parser must expose:

- streaming and bounded-memory operation where practical;
- strict and permissive modes;
- structured diagnostics;
- source byte offsets when meaningful;
- deterministic output;
- explicit handling of malformed records;
- fuzz and property tests;
- golden fixtures from legally distributable examples.

Python bindings expose typed batches or Arrow-compatible structures. They do not leak Rust implementation internals into model code.

### 11.3 Scientific semantics stay above parsing

Parsing answers, “What does the source file contain?”

Scientific normalization answers, “What does this record mean for Mindclade's model and dataset contract?”

Do not combine them. Source-faithful parsed records should remain available for audit and reprocessing.

---

## 12. Data platform architecture

### 12.1 Immutable pipeline stages

```text
Source descriptor
    -> raw object
    -> parsed record batch
    -> normalized snapshot
    -> curated dataset
    -> deduplicated/leakage-audited dataset
    -> split
    -> model feature dataset
```

Every arrow is a versioned transformation with:

- code revision;
- configuration digest;
- input digest set;
- output digest set;
- schema version;
- toolchain/runtime identity;
- validation report;
- policy classification;
- timestamps and actor identity;
- retry/idempotency key.

Do not mutate a published dataset version. Produce a new version.

### 12.2 Connector contract

Every source adapter implements the same lifecycle:

```text
discover -> plan -> fetch -> verify -> parse -> normalize -> publish
```

The adapter must support:

- resumable pagination/downloads;
- source rate limits and terms;
- conditional fetch or source revision detection;
- checksums and size verification;
- deterministic source object naming;
- idempotent replay;
- deletion/tombstone semantics;
- source-specific metadata;
- offline fixture mode for CI.

PDB, UniProt, RNACentral, and CCD are adapters, not bespoke pipeline frameworks.

### 12.3 Storage split

Use:

- object storage for raw source files, normalized shards, features, checkpoints, models, reports, and large logs;
- a relational metadata store for jobs, catalog entries, ownership, policy, lineage indexes, and artifact references;
- a queue or durable workflow substrate for execution;
- a cache only for reconstructible acceleration.

Never store model weights or full datasets in the relational database. Never treat an object-store prefix as the only source of catalog truth.

### 12.4 Content-addressed artifact reference

All large artifacts use a stable reference concept:

```text
ArtifactRef
- namespace
- logical name
- media type
- digest algorithm
- digest
- size
- schema version
- storage locator
- encryption/policy metadata
- lineage reference
```

Logical aliases such as `latest` may exist in the catalog but must resolve to an immutable digest before execution.

### 12.5 Dataset qualification

A training-eligible dataset version must have:

- schema validation;
- source integrity validation;
- biological invariant checks;
- deduplication report;
- train/evaluation leakage report;
- license and source-terms record;
- safety/policy classification;
- split manifest;
- feature compatibility declaration;
- reproducibility record;
- dataset card.

---

## 13. Model architecture

### 13.1 Model packages are pure execution units

A model package owns:

- typed configuration;
- module graph;
- forward contracts;
- initialization;
- state-dict schema;
- checkpoint conversion;
- supported tasks;
- feature requirements;
- output semantics;
- reference tests;
- numerical qualification;
- model card metadata.

It does not own:

- cluster launch;
- experiment database writes;
- queue consumption;
- HTTP handlers;
- environment-specific storage credentials.

### 13.2 Model component boundaries

Keep reusable model components under `models/components/`, but only after at least two real model consumers exist. Otherwise, keep the component inside the model family to avoid speculative abstraction.

Likely shared components include:

- token and geometric embeddings;
- Pairformer-style blocks;
- diffusion modules;
- confidence heads;
- geometric transforms;
- mixture-of-experts layers;
- output heads and loss primitives.

Kernel-backed components must retain a correct framework reference path for qualification.

### 13.3 Model bundle

A released model bundle contains or references:

- immutable weight shards;
- typed model configuration;
- model family and version;
- state-dict/checkpoint schema version;
- feature schema requirements;
- tokenizer/vocabulary/chemical component versions;
- precision and hardware compatibility;
- qualified kernel signatures;
- code revision and build provenance;
- evaluation report digest;
- safety policy metadata;
- license and distribution policy;
- model card.

No serving worker should infer these values from filenames.

---

## 14. Training architecture

Mindclade owns the trainer contract, training state, topology policy, sharding plans, checkpoint schema, data semantics, and numerical qualification. Execution engines consume these contracts.

### 14.1 Core contracts

```python
class TrainingTask(Protocol):
    def build_model(self, context: ModelBuildContext) -> Model: ...
    def build_data(self, context: DataBuildContext) -> DataSource: ...
    def compute_loss(
        self,
        model: Model,
        batch: Batch,
        context: StepContext,
    ) -> LossOutput: ...
    def evaluators(self) -> Sequence[Evaluator]: ...
    def checkpointables(self) -> Mapping[str, Checkpointable]: ...
```

```python
class TrainingEngine(Protocol):
    def initialize(
        self,
        task: TrainingTask,
        recipe: TrainingRecipe,
        topology: Topology,
    ) -> EngineState: ...

    def run(self, state: EngineState) -> TrainingResult: ...
```

```python
class ParallelPlan(Protocol):
    def validate(self, model, topology, hardware) -> ValidationReport: ...
    def apply(self, model, mesh) -> ParallelizedModel: ...
```

The exact Python signatures may evolve, but the separation is mandatory.

### 14.2 Required first-class capabilities

- arbitrary checkpointable component registration;
- optimizer construction with model, topology, precision, and parameter-group context;
- FSDP, tensor, pipeline, context, and expert parallel planning;
- MoE routing losses, reductions, capacity policy, load telemetry, and expert checkpoint semantics;
- diffusion timestep/noise objectives, deterministic RNG streams, EMA, and sampling evaluation;
- activation checkpoint policy;
- precision policy and loss scaling;
- deterministic seed hierarchy;
- elastic or restart-aware state;
- callback/hook lifecycle with explicit ordering;
- failure-safe checkpoint commit;
- evaluation scheduling;
- structured training events.

### 14.3 Engine strategy

Primary production engine:

- native PyTorch distributed primitives and a TorchTitan-aligned engine.

Secondary engine:

- Lightning Fabric for single-node/developer ergonomics and telemetry adaptation.

The Fabric path must not become a second distributed control plane layered over the production engine. Both engines consume the same `TrainingTask`, `TrainingState`, recipe, evaluation, and checkpoint contracts.

Optional providers such as Transformer Engine, Megatron Core, or TorchAO live behind narrow adapters. Model packages must not directly depend on them unless a model-specific capability requires it and the dependency is recorded.

### 14.4 Distributed policy

Model code describes mathematical structure. A separate plan describes how it is partitioned.

```text
model
+ task
+ hardware topology
+ precision policy
+ parallel plan
= executable distributed program
```

Validate before launch:

- world-size divisibility;
- mesh dimensions;
- sequence and atom bucket compatibility;
- expert count and capacity;
- pipeline stage balance;
- checkpoint reshard support;
- optimizer compatibility;
- deterministic RNG partitioning;
- kernel availability on target architecture;
- estimated memory headroom.

### 14.5 Checkpoint architecture

Checkpointing is a subsystem, not a `torch.save` call.

A checkpoint commit includes:

- model state;
- optimizer and scheduler state;
- scaler/precision state;
- RNG streams;
- data iterator/sampler state;
- task-specific checkpointables;
- EMA state;
- topology and parallel-plan metadata;
- code/configuration digests;
- step/tokens/examples counters;
- lineage and parent checkpoint;
- integrity manifest;
- completion marker written only after all shards are durable.

Required behavior:

- asynchronous save with bounded staging memory;
- atomic publication;
- save/load planners;
- load-time resharding;
- partial load by named component;
- format migration;
- corruption detection;
- retention policy;
- resume validation;
- conversion to release model bundles.

### 14.6 Recipes

Recipes are typed, validated, versioned configurations. They are not arbitrary YAML bags.

A recipe references immutable:

- model configuration;
- dataset/feature versions;
- objective;
- optimizer and schedule;
- precision policy;
- parallel plan;
- checkpoint policy;
- evaluation suite;
- resource profile.

Secrets, cluster names, and mutable storage paths are injected by the execution environment, not embedded in recipes.

---

## 15. Kernel architecture

### 15.1 Kernel package contract

Every optimized operation provides:

```text
reference implementation
optimized implementation
shape/dtype/layout capability declaration
dispatch policy
autotuning search space
correctness tests
gradient tests
determinism tests
hardware qualification
benchmarks
fallback policy
```

### 15.2 Registry key

A kernel qualification key should include at least:

```text
operation
implementation version
input/output dtypes
accumulation dtype
shape or shape family
layout/strides
mask/bias mode
device architecture
compiler/toolchain version
determinism mode
numerical tolerance profile
```

A benchmark result without this key is not actionable.

### 15.3 Dispatch policy

Production dispatch must be explicit:

1. Resolve operation signature.
2. Select only implementations qualified for the current signature and hardware.
3. Apply policy constraints such as deterministic mode.
4. Record selected implementation in diagnostics.
5. Fail clearly or use an explicitly approved reference fallback.

Never silently use a slower or numerically different path in a production qualification run.

### 15.4 Qualification gates

For each supported signature:

- forward parity;
- backward/gradient parity;
- finite-difference or high-precision checks where appropriate;
- randomized and adversarial shape coverage;
- NaN/Inf behavior;
- determinism when claimed;
- memory safety;
- race detection where available;
- performance floor versus the accepted baseline;
- compilation-cache behavior;
- clean-process reproducibility.

Benchmarks are stored as structured artifacts and compared statistically. A single best timing is not a release gate.

---

## 16. Evaluation architecture

Evaluation is independent of training loops and serving APIs.

An evaluation suite defines:

- immutable dataset references;
- input transformation;
- model/inference contract;
- metrics;
- aggregation;
- uncertainty/statistical method;
- pass/fail thresholds;
- report schema;
- reproducibility settings;
- safety policy.

### Evaluation classes

- unit numerical checks;
- model-component parity;
- model-family regression;
- structure and complex prediction quality;
- sequence representation/generation;
- molecular design objectives;
- confidence calibration;
- robustness and perturbation;
- data leakage;
- runtime performance;
- distributed consistency;
- safety and policy qualification.

Every model release references an immutable evaluation report digest. Dashboard state is not the release evidence.

---

## 17. Inference architecture

Separate pure model execution from network serving.

`inference/` owns:

- request-to-feature conversion;
- bucketing and batching policy;
- model execution;
- diffusion/sample orchestration;
- confidence computation;
- ranking;
- postprocessing;
- artifact production;
- execution diagnostics.

`services/runtime_gateway` owns:

- authentication and authorization;
- request validation;
- tenancy and quotas;
- durable job creation;
- streaming/status protocol;
- routing;
- public error mapping.

`workers/inference_worker` owns:

- queue/lease integration;
- GPU process lifecycle;
- model bundle acquisition;
- invocation of `inference/`;
- heartbeats and cancellation;
- artifact upload;
- operational telemetry.

### Reference asynchronous request flow

```text
client
  -> runtime gateway
  -> validate and authorize
  -> durable inference job
  -> data/feature preparation
  -> feature artifact
  -> resource-aware admission
  -> inference worker
  -> model trunk and generative sampling
  -> confidence and ranking
  -> immutable output artifacts
  -> job completion event
  -> SDK presents result
```

Large results are artifact references, not embedded database rows or queue messages.

---

## 18. Service and worker architecture

### 18.1 Start with a modular control-plane monolith

The initial Go control plane should contain clear modules for:

- tenants/projects/users;
- datasets;
- artifacts;
- experiments/runs;
- jobs;
- models/checkpoints;
- policy;
- audit.

Each module owns:

- domain types;
- application commands/queries;
- repository interfaces;
- protocol adapters;
- authorization checks;
- tests.

Modules may share platform infrastructure but not each other's database tables directly. Use explicit module APIs or events.

Split a module into a separate service only when one or more are true:

- distinct scaling profile;
- distinct trust boundary;
- independent availability requirement;
- independent release ownership;
- data sovereignty requirement;
- operational load is harming the monolith;
- team ownership makes the boundary durable.

### 18.2 Durable job state

Use an explicit state machine such as:

```text
PENDING
-> VALIDATING
-> QUEUED
-> ADMITTED
-> RUNNING
-> SUCCEEDED

Any active state
-> CANCELLING
-> CANCELLED

Any active state
-> RETRY_WAIT
-> QUEUED

Any active state
-> FAILED
```

Transitions are compare-and-swap or transactional. Each transition emits an audit record and an outbox event.

### 18.3 Queue and lease contract

Workers use:

- idempotency keys;
- visibility/lease timeout;
- heartbeat;
- bounded retry;
- poison-job handling;
- cancellation;
- attempt identity;
- progress checkpoints;
- immutable input references;
- result manifest;
- failure classification.

A worker must tolerate duplicate delivery. “Exactly once” is not assumed across distributed infrastructure.

### 18.4 Outbox before event-service proliferation

Use a transactional outbox in the control plane before introducing a separate event dispatcher. Split dispatch when throughput, delivery isolation, or ownership justifies it.

Do not create a standalone “health service.” Every deployable exposes standardized health, readiness, metrics, and diagnostics endpoints through shared service libraries.

---

## 19. SDK and application architecture

### 19.1 SDK layers

Each SDK has:

1. generated protocol client;
2. transport/authentication layer;
3. typed public resource models;
4. ergonomic high-level client;
5. polling/streaming helpers;
6. artifact upload/download helpers;
7. error hierarchy;
8. conformance tests;
9. examples and API documentation.

Generated protocol code is not the public SDK surface.

### 19.2 Application dependency rule

Applications consume the TypeScript SDK and design system. They do not:

- query service databases;
- import Protobuf-generated code throughout feature components;
- know Kubernetes/job implementation details;
- encode business authorization in the browser;
- duplicate model/dataset state machines.

### 19.3 Initial product surfaces

- `console`: model runs, datasets, training, evaluation, artifacts, deployments, usage, and developer workflows;
- `admin`: tenancy, policy, audit, quotas, support, and incident operations;
- `docs`: SDK documentation, API reference, tutorials, model/dataset cards, and platform concepts.

Keep `admin` separate only when its trust boundary and deployment policy are materially different; otherwise begin as a protected console area.

---

## 20. Research graduation policy

`research/` is intentionally permissive but isolated.

Allowed:

- notebooks;
- one-off studies;
- prototypes;
- ablations;
- exploratory datasets represented only by references;
- paper reproduction.

Not allowed:

- production services importing research code;
- notebooks as training launchers for official runs;
- committed large outputs;
- hidden dependencies installed manually;
- production model checkpoints without manifests;
- secrets or restricted data.

### Graduation path

```text
research prototype
-> reproducible experiment
-> named owner and design note
-> domain package implementation
-> unit/parity tests
-> integration with build graph
-> qualification suite
-> production recipe/service adoption
```

Graduated code leaves `research/`; do not maintain two authoritative implementations.

---

## 21. CI architecture

### 21.1 GitHub Actions

Use GitHub Actions for fast, organization-integrated checks:

- PR metadata and policy;
- CODEOWNERS/approval validation;
- lightweight formatting and configuration validation;
- docs links/build smoke test;
- Protobuf breaking-change signal;
- dependency review;
- required-check aggregation;
- Buildkite trigger/status bridge;
- mirror verification and repository administration.

Do not run expensive GPU or large distributed qualification on shared GitHub-hosted runners.

### 21.2 Buildkite

Buildkite is authoritative for:

- Bazel affected-target planning;
- CPU builds and tests;
- remote cache/execution;
- GPU tests and kernel qualification;
- distributed training/inference smoke tests;
- large integration suites;
- nightly data/model validation;
- clean-checkout release qualification;
- OCI/wheel/npm/binary/model-bundle publication;
- provenance, SBOM, signing, and attestations.

Generate a dynamic pipeline from:

- changed files;
- reverse dependency graph;
- component metadata;
- trust context;
- target tags;
- release intent.

Persist the generated pipeline as an artifact so every build can be audited.

### 21.3 Pipeline stages

```text
1. repository metadata and trust validation
2. protocol/schema compatibility
3. affected target calculation
4. formatting, linting, type checks, unit tests
5. builds and package tests
6. domain contract/conformance tests
7. integration and service tests
8. numerical/kernel/GPU qualification when affected
9. distributed and failure tests when affected
10. release packaging
11. SBOM, signing, provenance, policy verification
12. publish immutable artifacts
```

### 21.4 Test tags

Standard Bazel tags:

```text
small
medium
large
network
integration
gpu
gpu-h100
gpu-h200
gpu-b200
distributed
exclusive
flaky-quarantine
numerical
kernel
performance
release
```

A quarantined flaky test still runs on a visible lane and has an owner and expiry. It is never silently removed from CI.

### 21.5 Trusted and untrusted builds

Untrusted pull requests:

- receive no production secrets;
- cannot write shared release caches;
- cannot publish artifacts;
- use isolated workers and cache namespaces;
- have restricted network access;
- cannot execute arbitrary privileged deployment logic.

Trusted protected-branch and release builds use OIDC/workload identity rather than long-lived cloud keys.

---

## 22. Test and qualification matrix

| Layer | Required evidence |
|---|---|
| Library | Unit, property, error-path, API compatibility, static analysis |
| Parser | Golden, malformed input, streaming, fuzz, round-trip where meaningful, cross-language conformance |
| Data connector | Offline fixtures, pagination, retry, resume, checksum, idempotency, source-change handling |
| Feature pipeline | Schema, invariants, deterministic output, Python/Rust parity, leakage and quality checks |
| Kernel | Reference parity, gradients, determinism, shapes, dtype/layout, hardware, performance |
| Model component | Forward/backward, checkpoint schema, initialization, numerical regression |
| Model family | End-to-end smoke, checkpoint load, distributed consistency, evaluation regression |
| Training | Resume, reshard, failure recovery, deterministic seed policy, optimizer/state correctness |
| Inference | Batching equivalence, cancellation, artifact correctness, performance, memory bounds |
| Service | Contract, authorization, migration, idempotency, outbox, failure injection |
| Worker | Duplicate delivery, lease loss, cancellation, restart, partial artifact cleanup |
| SDK | Generated drift, public API, transport errors, pagination/streaming, conformance |
| Deployment | Schema, policy, server-side validation, rollout/rollback, health |
| Release | Clean checkout, artifact digest, SBOM, signature, provenance, install/run smoke |

### Numerical baselines

Numerical baselines include:

- input generation and seed;
- exact package/toolchain versions;
- hardware class;
- precision mode;
- tolerance rationale;
- expected statistical distribution when exact equality is inappropriate;
- owner and review date.

Never update a numerical golden merely because a test failed. The change requires evidence and review.

---

## 23. Release and artifact model

There is no monorepo version.

| Artifact | Version identity |
|---|---|
| Internal service/worker image | Git revision plus immutable OCI digest |
| Python/TypeScript public SDK | Semantic version |
| Go/Rust internal library | Source revision; public extraction gets independent semantic version |
| Protobuf API | Package version plus compatibility baseline |
| Dataset | Immutable logical version plus content digest |
| Feature dataset | Feature schema version plus source/config digest |
| Checkpoint | Checkpoint schema plus content digest and parent lineage |
| Model bundle | Model family version plus immutable manifest digest |
| Kernel bundle | Implementation/toolchain digest plus qualification matrix |
| Deployment package | Package version/digest; environment promotion references immutable artifacts |

### Release manifest

Every release job emits a manifest containing:

- source revision;
- build target;
- dependencies/lockfile digests;
- toolchain identity;
- output artifacts and digests;
- SBOM references;
- provenance/attestation references;
- test and qualification report digests;
- signer/build identity;
- promotion eligibility.

Promotion copies or references the same artifact. It never rebuilds from source for each environment.

---

## 24. Kubernetes and workload execution

Use Kubernetes as an execution substrate, not the source of business truth.

### 24.1 Workload classes

- long-running control-plane services;
- stateless gateways;
- CPU ingestion/preprocessing jobs;
- distributed GPU training;
- GPU evaluation;
- online and asynchronous inference;
- maintenance and conversion jobs.

### 24.2 Scheduling pattern

- Kueue owns quota admission, cohorts, priority, and resource sharing.
- JobSet or the chosen distributed-training API groups coordinated jobs.
- Device plugins advertise GPU and specialized device resources.
- The Mindclade control plane creates durable logical jobs and desired workload specifications.
- Kubernetes status is observed and reconciled into Mindclade job state; it is not the sole durable job record.

### 24.3 Deployment flow

```text
monorepo release
  -> immutable image/package/model digests
  -> release manifest
  -> gitops promotion pull request
  -> Argo CD/ApplicationSet reconciliation
  -> environment health and policy gates
```

Use Argo CD projects to constrain source repositories, destinations, and resource kinds. Use ApplicationSets for repeated multi-cluster/environment generation. The GitOps repository owns the actual environment mapping.

---

## 25. Observability

Use OpenTelemetry-compatible traces, metrics, and logs across Go, Rust, Python, and TypeScript.

### 25.1 Correlation context

Propagate:

- trace context;
- request ID;
- job ID;
- run ID;
- tenant/project identity;
- model manifest digest;
- dataset/feature manifest digest;
- checkpoint digest;
- code revision;
- worker attempt;
- selected kernel signature where relevant.

Do not put unbounded run IDs, artifact digests, sequences, or customer identifiers into metric labels. Use traces, structured logs, or exemplars for high-cardinality correlation.

### 25.2 ML telemetry

Training and evaluation telemetry includes:

- step/tokens/examples;
- objective components;
- optimizer and gradient statistics;
- precision/loss-scale state;
- data throughput and starvation;
- communication/computation time;
- memory;
- MoE routing/capacity/load balance;
- checkpoint latency and backlog;
- evaluation metrics;
- numerical anomalies;
- kernel dispatch and compilation events.

ML telemetry writes through an adapter. Training code must continue safely when a non-critical dashboard backend is unavailable, while preserving local durable event output.

### 25.3 Logging policy

Never log:

- raw biological sequences by default;
- structure payloads;
- model weights;
- credentials or signed URLs;
- restricted dataset contents;
- full user prompts/inputs without explicit policy.

Log stable identifiers and digest references instead.

---

## 26. Security, supply chain, and biological governance

### 26.1 Data classifications

At minimum:

- public;
- internal;
- confidential;
- restricted biological;
- regulated human-derived;
- secrets/credentials.

Each component declares the classifications it handles. Policy controls execution environment, storage, egress, logging, retention, and operator access.

### 26.2 Repository controls

- protected `main`;
- required reviews and CODEOWNERS;
- signed release tags or equivalent protected release identity;
- secret scanning;
- dependency and license review;
- static analysis;
- restricted workflow permissions;
- pinned third-party CI actions/plugins;
- isolated untrusted CI;
- no long-lived cloud credentials;
- reproducible clean-checkout releases.

### 26.3 Artifact controls

- content digests;
- encryption in transit and at rest;
- least-privilege access;
- immutable publication;
- SBOMs for software artifacts;
- provenance and build attestations;
- signatures for release artifacts;
- admission verification before deployment;
- retention and legal-hold support where required;
- audit receipts for access and promotion.

### 26.4 Biological safeguards

- source terms and license metadata are mandatory;
- restricted sequences and safety corpora are never committed to Git;
- high-risk datasets use isolated projects/buckets and explicit egress policy;
- model release manifests include safety evaluation evidence;
- generated biological payloads follow the same classification controls as source data;
- human-derived data requires separate review, minimization, and retention policy;
- production logs and traces contain references, not payloads.

---

## 27. Configuration architecture

Configuration has four categories:

1. **Code defaults**: safe, environment-independent defaults next to the owner.
2. **Typed recipes**: model/training/evaluation execution definitions in the monorepo.
3. **Deployment package defaults**: service-owned, non-secret operational defaults.
4. **Environment desired state**: lives in `gitops`, not the monorepo.

Rules:

- every configuration is schema-validated;
- unknown fields fail;
- secrets are references, never values in Git;
- mutable aliases resolve to immutable references before execution;
- configuration digests are recorded in job and artifact manifests;
- environment variables are an injection mechanism, not an undocumented configuration API;
- flags are reserved for operator overrides and debugging, not hundreds of permanent settings.

---

## 28. Database and migration policy

- The control plane owns the operational relational schema.
- Migrations are forward-only by default and tested from supported historical states.
- Every migration has an owner, compatibility window, and rollback/repair procedure.
- Deployments follow expand/migrate/contract for incompatible schema changes.
- Workers do not query control-plane tables directly; they use APIs or queue contracts.
- Analytical/event exports use explicit pipelines rather than operational replicas becoming undocumented APIs.
- Artifact data remains outside relational rows.
- Audit records are append-oriented and protected against casual mutation.

---

## 29. Ownership and governance

### 29.1 Ownership layers

- central `.github/CODEOWNERS`;
- `component.yaml` owner;
- package README owner;
- service/runbook on-call owner for production components;
- model/data/kernel qualification owner.

CI fails when a production component has no valid owner.

### 29.2 ADRs

Use `docs/adr/` for decisions that change:

- top-level boundaries;
- protocol compatibility;
- storage formats;
- training/checkpoint contracts;
- kernel dispatch policy;
- security trust boundaries;
- release semantics;
- infrastructure repository ownership.

ADRs describe context, decision, alternatives, consequences, and migration. They do not duplicate implementation documentation.

### 29.3 Maturity labels

Recommended component maturity:

```text
experimental
incubating
supported
production
deprecated
retired
```

Maturity controls required tests, compatibility promises, owner expectations, and release eligibility.

---

## 30. Developer workflow

### First checkout

```bash
nix develop
just doctor
just bootstrap
just test-affected
```

A developer without Nix may use documented native setup, but CI and release behavior are defined by pinned toolchains.

### Normal change

```bash
just format
just lint
just test-affected
just build-affected
```

### Model change

```bash
just test //models/...
just test //kernels/... --config=gpu
just train-smoke
just inference-smoke
just evaluation-smoke
```

### Protocol change

```bash
just proto
bazel test //protocols/...
```

### Release qualification

```bash
just release-check
```

Local commands never publish or deploy by default.

---

## 31. What to implement immediately

### Foundation

- root Bazel/Bzlmod, Nix, uv, Cargo, Go, pnpm, and Buf configuration;
- shared repository metadata and `component.yaml` schema;
- architecture/dependency policy tests;
- fast Buildkite affected-target planner;
- lightweight GitHub required-check workflow;
- protocol lint/breaking checks;
- artifact, identifier, configuration, observability, and testing libraries;
- content-addressed artifact manifest.

### Biological/data core

- canonical biological schemas;
- Rust `bio-entities` and `bio-formats` implementation;
- Python bindings and conformance fixtures;
- connector API;
- PDB, UniProt, RNACentral, and CCD adapters;
- immutable source/snapshot lineage and data validation.

### Model/training core

- model API and one model family package;
- reference Pairformer/diffusion components;
- kernel API, registry, dispatch, and first qualified TileLang kernels;
- `TrainingTask`, engine, state, parallel plan, optimizer context, and callback contracts;
- production checkpoint subsystem;
- smoke recipes and evaluation harness.

### Platform core

- Go control-plane modular monolith;
- runtime gateway;
- ingestion, training, evaluation, and inference workers;
- Python and TypeScript SDKs;
- initial console;
- service-owned deployment bases;
- end-to-end asynchronous job flow.

---

## 32. What to defer

Defer until measurable need exists:

- splitting every control-plane module into a service;
- custom distributed scheduler;
- custom workflow engine;
- custom feature-store product;
- service mesh;
- multi-cloud abstraction;
- public Go and Rust SDKs;
- model marketplace;
- user-extensible kernel plugin system;
- independent event dispatcher;
- standalone webhook service;
- on-premises packaging;
- multiple Python lock universes;
- many Go modules;
- checking all generated code into Git;
- a second source of truth for experiment/model metadata.

The blueprint reserves clean seams for these capabilities without paying their operational cost today.

---

## 33. Repository anti-patterns

Reject these during review:

- a new top-level directory without an architecture owner;
- `common`, `utils`, or `helpers` packages with unrelated content;
- domain code in CI scripts;
- model code inside a worker entrypoint;
- service implementation imported by an SDK;
- a Python package depending on a Go binary for library behavior;
- hidden network access in builds or tests;
- mutable `latest` references in production recipes;
- environment-specific values in model/data manifests;
- direct object-store path construction outside the artifact library;
- silently caught exceptions that change numerical behavior;
- unqualified optimized kernels;
- checkpoints without schema and integrity manifests;
- datasets without lineage and policy metadata;
- notebook-only production procedures;
- per-library Go modules;
- separate lockfiles without a real release/environment boundary;
- generated API models edited by hand;
- infrastructure-live or GitOps environment state copied into the monorepo;
- an empty scaffold presented as production capability.

---

## 34. Final architecture rules

Adopt these as the concise Mindclade monorepo constitution:

1. **Organize by domain; implement with the language best suited to the domain.**
2. **Use contracts across processes and languages, never accidental shared implementation.**
3. **Keep foundational libraries small, horizontal, and dependency-light.**
4. **Keep `libs/python` free of PyTorch and GPU dependencies.**
5. **Keep model mathematics independent of training engines and serving processes.**
6. **Keep training policy independent of any one execution provider.**
7. **Qualify optimized kernels against maintained reference implementations.**
8. **Treat datasets, features, checkpoints, models, and reports as immutable artifacts with lineage.**
9. **Start with a modular control-plane monolith and specialized workers.**
10. **Use Bazel as the integration graph and native lockfiles as ecosystem dependency truth.**
11. **Build once, attest once, and promote immutable artifacts through GitOps.**
12. **Keep live cloud and environment desired state outside the source monorepo.**
13. **Make ownership, compatibility, security classification, and qualification machine-readable.**
14. **Allow research freedom, but require an explicit graduation path into production.**
15. **Prefer fewer complete components over a large tree of unimplemented promises.**

---

## 35. Technology basis

This blueprint is intentionally version-agnostic at the document level; exact versions must be pinned in repository lockfiles and upgraded through qualification. The architecture aligns with the current official capabilities and guidance of:

- Bazel Bzlmod: <https://bazel.build/external/overview>
- PyTorch distributed overview, DeviceMesh/DTensor, FSDP2, and distributed checkpointing:
  - <https://docs.pytorch.org/tutorials/beginner/dist_overview.html>
  - <https://docs.pytorch.org/docs/stable/distributed.checkpoint.html>
- uv workspaces: <https://docs.astral.sh/uv/concepts/projects/workspaces/>
- Cargo workspaces: <https://doc.rust-lang.org/cargo/reference/workspaces.html>
- Go modules/workspaces: <https://go.dev/ref/mod>
- pnpm workspaces: <https://pnpm.io/workspaces>
- Buf linting and breaking-change detection: <https://buf.build/docs/breaking/>
- OpenTelemetry signals and context propagation:
  - <https://opentelemetry.io/docs/concepts/signals/>
  - <https://opentelemetry.io/docs/concepts/context-propagation/>
- Kueue and JobSet:
  - <https://kueue.sigs.k8s.io/docs/overview/>
  - <https://jobset.sigs.k8s.io/>
- Argo CD cluster bootstrapping and ApplicationSets:
  - <https://argo-cd.readthedocs.io/en/stable/operator-manual/cluster-bootstrapping/>
  - <https://argo-cd.readthedocs.io/en/latest/user-guide/application-set/>
- Buildkite dynamic pipelines and monorepo practices:
  - <https://buildkite.com/docs/pipelines/configure/dynamic-pipelines>
  - <https://buildkite.com/docs/pipelines/best-practices/working-with-monorepos>
- Nix flakes and lockfiles:
  - <https://nixos.org/manual/nix/stable/command-ref/new-cli/nix3-flake-check.html>
  - <https://nixos.org/manual/nix/stable/command-ref/new-cli/nix3-flake-lock.html>
- SLSA provenance: <https://slsa.dev/spec/v1.2/>

---

**Recommended repository name:** `mindclade` for the canonical internal monorepo.  
**Recommended Git remote:** `github.com/Mindclade/mindclade`.  
**Recommended Go module:** `github.com/Mindclade/mindclade`.  
**Recommended Python namespace:** `mindclade.*`.  
**Recommended TypeScript scope:** `@mindclade/*`.  
**Recommended Protobuf namespace:** `mindclade.<domain>.v1`.  
**Recommended Kubernetes/API group:** `mindclade.dev`.

