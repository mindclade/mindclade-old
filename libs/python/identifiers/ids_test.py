from __future__ import annotations

import unittest

from libs.python.identifiers.ids import KINDS, is_valid, new_id, parse_id


class IdsTest(unittest.TestCase):
    def test_round_trip_every_kind(self) -> None:
        for kind in KINDS:
            value = new_id(kind)
            parsed_kind, suffix = parse_id(value)
            self.assertEqual(parsed_kind, kind)
            self.assertEqual(len(suffix), 32)
            self.assertTrue(is_valid(value))

    def test_unknown_kind_rejected(self) -> None:
        with self.assertRaises(ValueError):
            new_id("submarine")

    def test_malformed_values_invalid(self) -> None:
        for bad in ("", "ds", "ds_", "ds_XYZ", "zz_" + "a" * 32, "ds_" + "a" * 31):
            self.assertFalse(is_valid(bad), bad)

    def test_ids_are_unique(self) -> None:
        self.assertEqual(len({new_id("dataset") for _ in range(1000)}), 1000)


if __name__ == "__main__":
    unittest.main()
