from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

from .builder import ExcelWorkbookBuilder
from .models import AgentEvent, BuildResult
from .parser import InformationParser


class ExcelAgent:
    def __init__(self, parser: InformationParser | None = None, builder: ExcelWorkbookBuilder | None = None) -> None:
        self.parser = parser or InformationParser()
        self.builder = builder or ExcelWorkbookBuilder()

    def create_workbook(self, information: str, output_path: Path, title: str = "Reporte generado") -> Iterator[AgentEvent]:
        yield AgentEvent("thinking", "Analizando la informacion recibida.", 0.15)
        spec = self.parser.parse(information, title=title)

        total_rows = sum(table.row_count for table in spec.tables)
        yield AgentEvent(
            "planning",
            f"Plan listo: {len(spec.tables)} tabla(s), {total_rows} fila(s).",
            0.35,
            {"tables": len(spec.tables), "rows": total_rows},
        )

        for table in spec.tables:
            yield AgentEvent(
                "building",
                f"Construyendo '{table.title}' con {table.row_count} fila(s).",
                0.65,
                {"table": table.title},
            )

        saved_path = self.builder.build(spec, output_path)
        yield AgentEvent(
            "done",
            f"Excel creado en {saved_path}.",
            1.0,
            {"result": BuildResult(output_path=saved_path, spec=spec)},
        )
