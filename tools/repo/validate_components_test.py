from __future__ import annotations

import copy
import pathlib
import unittest

from validate_components import _in_bazel_output, validate_component

VALID = {
    "apiVersion": "mindclade.dev/v1",
    "kind": "Service",
    "metadata": {"name": "control-plane", "owner": "platform-control-plane"},
    "spec": {
        "maturity": "experimental",
        "tier": 1,
        "languages": ["go"],
        "buildTargets": ["//services/control_plane/cmd/control-plane"],
        "testTargets": ["//services/control_plane/..."],
        "artifacts": [{"type": "oci", "name": "control-plane"}],
        "protocols": ["mindclade.artifact.v1"],
        "dataClassifications": ["internal"],
        "runtime": {"kubernetes": True, "gpu": False},
    },
}


class ValidateComponentTest(unittest.TestCase):
    def test_valid_component_passes(self) -> None:
        self.assertEqual(validate_component(VALID), [])

    def test_missing_owner_fails(self) -> None:
        doc = copy.deepcopy(VALID)
        del doc["metadata"]["owner"]
        self.assertTrue(any("owner" in e for e in validate_component(doc)))

    def test_unknown_field_fails(self) -> None:
        doc = copy.deepcopy(VALID)
        doc["spec"]["surprise"] = True
        self.assertNotEqual(validate_component(doc), [])

    def test_production_maturity_requires_nonplaceholder_owner(self) -> None:
        doc = copy.deepcopy(VALID)
        doc["spec"]["maturity"] = "production"
        doc["metadata"]["owner"] = "TBD"
        self.assertTrue(any("owner" in e for e in validate_component(doc)))


class InBazelOutputTest(unittest.TestCase):
    def test_excludes_bazel_bin(self) -> None:
        root = pathlib.Path("/repo")
        path = pathlib.Path("/repo/bazel-bin/tools/repo/component.yaml")
        self.assertTrue(_in_bazel_output(root, path))

    def test_excludes_bazel_out(self) -> None:
        root = pathlib.Path("/repo")
        path = pathlib.Path("/repo/bazel-out/darwin_arm64-fastbuild/component.yaml")
        self.assertTrue(_in_bazel_output(root, path))

    def test_excludes_bazel_testlogs(self) -> None:
        root = pathlib.Path("/repo")
        path = pathlib.Path("/repo/bazel-testlogs/tools/repo/test.log")
        self.assertTrue(_in_bazel_output(root, path))

    def test_includes_regular_path(self) -> None:
        root = pathlib.Path("/repo")
        path = pathlib.Path("/repo/services/control_plane/component.yaml")
        self.assertFalse(_in_bazel_output(root, path))

    def test_includes_path_with_bazel_in_name_not_prefix(self) -> None:
        root = pathlib.Path("/repo")
        path = pathlib.Path("/repo/services/bazel_helper/component.yaml")
        self.assertFalse(_in_bazel_output(root, path))


if __name__ == "__main__":
    unittest.main()
