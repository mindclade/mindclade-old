from __future__ import annotations

import datetime
import json
import sys
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import IO, Any


@dataclass(frozen=True)
class BoundLogger:
    name: str
    stream: IO[str]
    context: Mapping[str, Any] = field(default_factory=dict)

    def bind(self, **fields: Any) -> BoundLogger:
        return BoundLogger(self.name, self.stream, {**self.context, **fields})

    def _emit(self, level: str, event: str, fields: Mapping[str, Any]) -> None:
        record = {
            "ts": datetime.datetime.now(datetime.UTC).isoformat(),
            "level": level,
            "logger": self.name,
            "event": event,
            **self.context,
            **fields,
        }
        self.stream.write(json.dumps(record, sort_keys=True) + "\n")

    def info(self, event: str, **fields: Any) -> None:
        self._emit("info", event, fields)

    def warning(self, event: str, **fields: Any) -> None:
        self._emit("warning", event, fields)

    def error(self, event: str, **fields: Any) -> None:
        self._emit("error", event, fields)


def get_logger(name: str, stream: IO[str] | None = None) -> BoundLogger:
    return BoundLogger(name, stream if stream is not None else sys.stderr)
