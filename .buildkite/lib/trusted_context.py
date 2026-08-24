from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class TrustContext:
    trusted: bool
    branch: str
    release_intent: bool

    @classmethod
    def from_environment(cls) -> TrustContext:
        pull_request = os.environ.get("BUILDKITE_PULL_REQUEST", "false") != "false"
        branch = os.environ.get("BUILDKITE_BRANCH", "")
        tag = os.environ.get("BUILDKITE_TAG", "")
        return cls(
            trusted=not pull_request,
            branch=branch,
            release_intent=bool(tag),
        )
