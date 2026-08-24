from __future__ import annotations

import copy
import unittest

from validate_components import validate_component

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


if __name__ == "__main__":
    unittest.main()
