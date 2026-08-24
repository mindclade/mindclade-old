from __future__ import annotations

import io
import json
import unittest

from libs.python.observability.logging import get_logger


class BoundLoggerTest(unittest.TestCase):
    def test_emits_json_line_with_bound_context(self) -> None:
        stream = io.StringIO()
        logger = get_logger("test", stream=stream).bind(job_id="job_" + "a" * 32)
        logger.info("job_admitted", attempt=1)
        record = json.loads(stream.getvalue().strip())
        self.assertEqual(record["event"], "job_admitted")
        self.assertEqual(record["level"], "info")
        self.assertEqual(record["job_id"], "job_" + "a" * 32)
        self.assertEqual(record["attempt"], 1)
        self.assertIn("ts", record)

    def test_bind_is_immutable(self) -> None:
        stream = io.StringIO()
        base = get_logger("test", stream=stream)
        base.bind(tenant="tn_" + "b" * 32)
        base.info("plain")
        record = json.loads(stream.getvalue().strip())
        self.assertNotIn("tenant", record)


if __name__ == "__main__":
    unittest.main()
