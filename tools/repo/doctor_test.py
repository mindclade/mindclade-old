from __future__ import annotations

import pathlib
import tempfile
import unittest

from doctor import compare_version, parse_pins


class ParsePinsTest(unittest.TestCase):
    def test_parses_all_repo_pins(self) -> None:
        root = pathlib.Path(tempfile.mkdtemp())
        (root / ".bazelversion").write_text("7.4.1\n")
        (root / ".python-version").write_text("3.12\n")
        (root / "package.json").write_text('{"packageManager": "pnpm@9.15.0"}\n')
        (root / "go.mod").write_text("module go.mindclade.dev/mindclade\n\ngo 1.23\n")
        (root / "rust-toolchain.toml").write_text('[toolchain]\nchannel = "1.84.0"\n')
        pins = parse_pins(root)
        self.assertEqual(pins["bazel"], "7.4.1")
        self.assertEqual(pins["python"], "3.12")
        self.assertEqual(pins["pnpm"], "9.15.0")
        self.assertEqual(pins["go"], "1.23")
        self.assertEqual(pins["rust"], "1.84.0")


class CompareVersionTest(unittest.TestCase):
    def test_prefix_match_accepts_patch_releases(self) -> None:
        self.assertTrue(compare_version("3.12", "3.12.13"))
        self.assertTrue(compare_version("7.4.1", "7.4.1"))

    def test_mismatch_rejected(self) -> None:
        self.assertFalse(compare_version("3.12", "3.11.9"))
        self.assertFalse(compare_version("9.15.0", "10.0.0"))


if __name__ == "__main__":
    unittest.main()
