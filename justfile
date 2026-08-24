set shell := ["bash", "-euo", "pipefail", "-c"]

default:
    @just --list

bootstrap:
    @echo "TODO: nix develop && uv sync && pnpm install"

doctor:
    @echo "TODO: verify pinned toolchains match lockfiles"

format:
    @echo "TODO: bazel run //tools/dev:format"

lint:
    @echo "TODO: bazel test //... --test_tag_filters=lint"

test:
    @echo "TODO: bazel test //..."

test-affected:
    @echo "TODO: bazel test \$(affected targets from .buildkite/lib/affected_targets.py)"

build:
    @echo "TODO: bazel build //..."

build-affected:
    @echo "TODO: bazel build \$(affected targets from .buildkite/lib/affected_targets.py)"

proto:
    @echo "TODO: buf lint && buf generate"

docs:
    @echo "TODO: bazel build //docs/..."

train-smoke:
    @echo "TODO: bazel run //training/recipes/smoke:run"

inference-smoke:
    @echo "TODO: bazel run //inference:smoke"

kernel-qualify:
    @echo "TODO: bazel test //kernels/... --config=gpu --test_tag_filters=kernel"

integration:
    @echo "TODO: bazel test //tests/integration/..."

release-check:
    @echo "TODO: bazel test //... --config=release (clean checkout qualification)"
