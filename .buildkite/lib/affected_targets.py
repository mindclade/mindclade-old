from __future__ import annotations


def affected_targets(base_revision: str, head_revision: str) -> list[str]:
    """Resolve changed files against the Bazel reverse dependency graph."""
    raise NotImplementedError
