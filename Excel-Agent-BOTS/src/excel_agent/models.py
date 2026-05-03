from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class AgentEvent:
    stage: str
    message: str
    progress: float
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class TableSpec:
    title: str
    headers: list[str]
    rows: list[list[Any]]

    @property
    def row_count(self) -> int:
        return len(self.rows)

    @property
    def column_count(self) -> int:
        return len(self.headers)


@dataclass(frozen=True)
class WorkbookSpec:
    title: str
    tables: list[TableSpec]
    notes: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class BuildResult:
    output_path: Path
    spec: WorkbookSpec
