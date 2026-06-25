from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class ActionItem:
    source: Path
    line: int
    kind: str
    status: str
    text: str
    owner: str | None
    tags: list[str]

    def to_json(self) -> dict[str, object]:
        data = asdict(self)
        data["source"] = self.source.as_posix()
        return data
