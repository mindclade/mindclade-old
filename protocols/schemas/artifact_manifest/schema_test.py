from __future__ import annotations

import json
import pathlib
import unittest

import jsonschema

HERE = pathlib.Path(__file__).resolve().parent


class ArtifactManifestSchemaTest(unittest.TestCase):
    def setUp(self) -> None:
        self.validator = jsonschema.Draft202012Validator(
            json.loads((HERE / "artifact_manifest.schema.json").read_text())
        )

    def test_valid_fixture_passes(self) -> None:
        doc = json.loads((HERE / "fixtures" / "valid_minimal.json").read_text())
        self.assertEqual(list(self.validator.iter_errors(doc)), [])

    def test_missing_digest_fails(self) -> None:
        doc = json.loads((HERE / "fixtures" / "invalid_missing_digest.json").read_text())
        self.assertNotEqual(list(self.validator.iter_errors(doc)), [])

    def test_unknown_field_fails(self) -> None:
        doc = json.loads((HERE / "fixtures" / "valid_minimal.json").read_text())
        doc["mutableAlias"] = "latest"
        self.assertNotEqual(list(self.validator.iter_errors(doc)), [])


if __name__ == "__main__":
    unittest.main()
