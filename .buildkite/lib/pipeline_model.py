from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Step:
    label: str
    command: str
    key: str
    agents: dict[str, str] = field(default_factory=dict)
    depends_on: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "label": self.label,
            "command": self.command,
            "key": self.key,
            "agents": self.agents,
            "depends_on": self.depends_on,
        }


@dataclass
class Pipeline:
    steps: list[Step]

    def to_dict(self) -> dict:
        return {"steps": [step.to_dict() for step in self.steps]}
