from __future__ import annotations

import unittest

from affected import affected_targets, to_label

UNIVERSE_FILES = ["MODULE.bazel", ".bazelrc", "uv.lock", "libs/python/BUILD.bazel"]


class AffectedTargetsTest(unittest.TestCase):
    def test_build_config_change_returns_universe(self) -> None:
        for name in UNIVERSE_FILES:
            self.assertEqual(affected_targets([name], query=self._fail_query), ["//..."])

    def test_source_change_maps_through_rdeps(self) -> None:
        calls = []

        def query(expr: str) -> list[str]:
            calls.append(expr)
            if expr.startswith("set("):
                return ["//libs/python:identifiers"]
            return ["//libs/python:identifiers", "//libs/python:artifacts_test"]

        result = affected_targets(["libs/python/identifiers/ids.py"], query=query)
        self.assertIn("//libs/python:artifacts_test", result)
        self.assertTrue(any("rdeps" in c for c in calls))

    def test_unowned_files_yield_no_targets(self) -> None:
        def query(expr: str) -> list[str]:
            return []

        self.assertEqual(affected_targets(["docs/README.md"], query=query), [])

    def _fail_query(self, expr: str) -> list[str]:
        raise AssertionError("query must not run for universe-triggering changes")


class ToLabelTest(unittest.TestCase):
    def test_owned_file_at_package_root(self) -> None:
        self.assertEqual(to_label("pkg/module.py", {"pkg"}), "//pkg:module.py")

    def test_owned_file_in_subdirectory_of_package(self) -> None:
        self.assertEqual(to_label("pkg/sub/deep/file.py", {"pkg"}), "//pkg:sub/deep/file.py")

    def test_unowned_file_returns_none(self) -> None:
        self.assertIsNone(to_label("other/file.py", {"pkg"}))

    def test_nearest_package_wins_over_shadowing_ancestor(self) -> None:
        self.assertEqual(to_label("pkg/sub/file.py", {"pkg", "pkg/sub"}), "//pkg/sub:file.py")

    def test_deleted_file_resolves_by_path_alone(self) -> None:
        self.assertEqual(to_label("pkg/sub/deleted.py", {"pkg", "pkg/sub"}), "//pkg/sub:deleted.py")


if __name__ == "__main__":
    unittest.main()
