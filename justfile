set shell := ["bash", "-euo", "pipefail", "-c"]

default:
    @just --list

bootstrap:
    uv sync --group dev
    pnpm install

doctor:
    python3 tools/repo/doctor.py

format:
    @echo "TODO: bazel run //tools/dev:format"

lint:
    @echo "TODO: bazel test //... --test_tag_filters=lint"

test:
    bazelisk test //...

test-affected:
    @echo "TODO: bazel test \$(affected targets from .buildkite/lib/affected_targets.py)"

build:
    bazelisk build //...

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
