from __future__ import annotations

import difflib
import os
import pathlib
import unittest


def assert_golden(test: unittest.TestCase, actual: str, golden_path: pathlib.Path) -> None:
    if os.environ.get("UPDATE_GOLDENS") == "1":
        golden_path.write_text(actual)
        return
    expected = golden_path.read_text()
    if actual != expected:
        diff = "".join(
            difflib.unified_diff(
                expected.splitlines(keepends=True),
                actual.splitlines(keepends=True),
                fromfile=str(golden_path),
                tofile="actual",
            )
        )
        test.fail(f"golden mismatch (set UPDATE_GOLDENS=1 to update deliberately):\n{diff}")
