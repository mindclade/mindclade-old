#!/usr/bin/env python3
"""Emit the dynamic Buildkite pipeline for this build.

Steps are selected from changed files, the reverse dependency graph, component
metadata, trust context, target tags, and release intent. The generated
pipeline is persisted as a build artifact for audit.
"""

from __future__ import annotations

import json
import sys

from lib.pipeline_model import Pipeline
from lib.trusted_context import TrustContext
from steps import gpu, nightly, presubmit, release, security


def main() -> int:
    context = TrustContext.from_environment()
    pipeline = Pipeline(steps=[])
    for module in (presubmit, security, gpu, nightly, release):
        pipeline.steps.extend(module.steps(context))
    json.dump(pipeline.to_dict(), sys.stdout, indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
