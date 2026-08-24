from __future__ import annotations

import pathlib
import tempfile
import unittest

from libs.python.testing.golden import assert_golden


class GoldenTest(unittest.TestCase):
    def test_matching_golden_passes(self) -> None:
        golden = pathlib.Path(tempfile.mkdtemp()) / "out.golden"
        golden.write_text("expected\n")
        assert_golden(self, "expected\n", golden)

    def test_mismatch_fails_with_diff(self) -> None:
        golden = pathlib.Path(tempfile.mkdtemp()) / "out.golden"
        golden.write_text("expected\n")
        with self.assertRaises(AssertionError):
            assert_golden(self, "surprise\n", golden)

    def test_update_mode_rewrites(self) -> None:
        golden = pathlib.Path(tempfile.mkdtemp()) / "out.golden"
        golden.write_text("old\n")
        import os

        os.environ["UPDATE_GOLDENS"] = "1"
        try:
            assert_golden(self, "new\n", golden)
        finally:
            del os.environ["UPDATE_GOLDENS"]
        self.assertEqual(golden.read_text(), "new\n")


if __name__ == "__main__":
    unittest.main()
