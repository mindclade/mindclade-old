from __future__ import annotations

import hashlib
import pathlib
import tempfile
import unittest

from libs.python.artifacts.refs import (
    ArtifactRef,
    ManifestError,
    from_manifest,
    sha256_file,
    to_manifest,
)


def _ref() -> ArtifactRef:
    return ArtifactRef(
        namespace="datasets",
        name="pdb-snapshot",
        media_type="application/zstd",
        digest_algorithm="sha256",
        digest_hex="a" * 64,
        size_bytes=42,
        storage_locator="gs://bucket/objects/aa",
        classification="internal",
    )


class ArtifactRefTest(unittest.TestCase):
    def test_manifest_round_trip(self) -> None:
        ref = _ref()
        self.assertEqual(from_manifest(to_manifest(ref)), ref)

    def test_uri_format(self) -> None:
        self.assertEqual(_ref().uri, "mindclade://datasets/pdb-snapshot@sha256:" + "a" * 64)

    def test_invalid_manifest_rejected(self) -> None:
        doc = to_manifest(_ref())
        doc["digest"]["hex"] = "not-hex"
        with self.assertRaises(ManifestError):
            from_manifest(doc)

    def test_unknown_field_rejected(self) -> None:
        doc = to_manifest(_ref())
        doc["latest"] = True
        with self.assertRaises(ManifestError):
            from_manifest(doc)

    def test_sha256_file_streams(self) -> None:
        with tempfile.NamedTemporaryFile(delete=False) as handle:
            handle.write(b"mindclade")
        path = pathlib.Path(handle.name)
        self.assertEqual(sha256_file(path), hashlib.sha256(b"mindclade").hexdigest())

    def test_float_sizeBytes_rejected(self) -> None:
        doc = to_manifest(_ref())
        doc["sizeBytes"] = 42.0
        with self.assertRaises(ManifestError):
            from_manifest(doc)

    def test_bool_sizeBytes_rejected(self) -> None:
        doc = to_manifest(_ref())
        doc["sizeBytes"] = True
        with self.assertRaises(ManifestError):
            from_manifest(doc)


if __name__ == "__main__":
    unittest.main()
