from __future__ import annotations

import csv
import re
from io import StringIO
from typing import Any

from .models import TableSpec, WorkbookSpec


class InformationParser:
    """Convierte informacion libre en una especificacion simple de Excel."""

    def parse(self, text: str, title: str = "Reporte generado") -> WorkbookSpec:
        cleaned = text.strip()
        if not cleaned:
            return WorkbookSpec(
                title=title,
                tables=[TableSpec("Datos", ["Elemento", "Detalle"], [])],
                notes=["No se recibio informacion para convertir."],
            )

        if self._looks_like_markdown_table(cleaned):
            table = self._parse_markdown_table(cleaned)
        elif self._looks_like_delimited(cleaned):
            table = self._parse_delimited(cleaned)
        elif self._looks_like_key_values(cleaned):
            table = self._parse_key_values(cleaned)
        else:
            table = self._parse_lines(cleaned)

        return WorkbookSpec(title=title, tables=[table])

    def _looks_like_markdown_table(self, text: str) -> bool:
        lines = [line for line in text.splitlines() if line.strip()]
        return len(lines) >= 2 and "|" in lines[0] and re.search(r"\|\s*:?-{3,}:?\s*\|", lines[1]) is not None

    def _looks_like_delimited(self, text: str) -> bool:
        first_line = text.splitlines()[0]
        return "," in first_line or ";" in first_line or "\t" in first_line

    def _looks_like_key_values(self, text: str) -> bool:
        lines = [line for line in text.splitlines() if line.strip()]
        return bool(lines) and all((":" in line or "=" in line) for line in lines)

    def _parse_markdown_table(self, text: str) -> TableSpec:
        lines = [line.strip().strip("|") for line in text.splitlines() if line.strip()]
        headers = self._normalize_headers([cell.strip() for cell in lines[0].split("|")])
        rows = [
            self._normalize_row([cell.strip() for cell in line.split("|")], len(headers))
            for line in lines[2:]
        ]
        return TableSpec("Tabla", headers, rows)

    def _parse_delimited(self, text: str) -> TableSpec:
        sample = text[:2048]
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
        reader = csv.reader(StringIO(text), dialect)
        records = [row for row in reader if any(cell.strip() for cell in row)]
        if not records:
            return TableSpec("Datos", ["Elemento", "Detalle"], [])

        headers = self._normalize_headers(records[0])
        rows = [self._normalize_row(row, len(headers)) for row in records[1:]]
        return TableSpec("Tabla", headers, rows)

    def _parse_key_values(self, text: str) -> TableSpec:
        rows: list[list[Any]] = []
        for line in text.splitlines():
            if not line.strip():
                continue
            key, value = re.split(r"[:=]", line, maxsplit=1)
            rows.append([key.strip(), self._coerce_value(value.strip())])
        return TableSpec("Resumen", ["Campo", "Valor"], rows)

    def _parse_lines(self, text: str) -> TableSpec:
        rows = [[index, line.strip()] for index, line in enumerate(text.splitlines(), start=1) if line.strip()]
        return TableSpec("Notas organizadas", ["#", "Informacion"], rows)

    def _normalize_headers(self, headers: list[str]) -> list[str]:
        normalized: list[str] = []
        for index, header in enumerate(headers, start=1):
            clean = header.strip() or f"Columna {index}"
            normalized.append(clean)
        return normalized

    def _normalize_row(self, row: list[str], size: int) -> list[Any]:
        values = [self._coerce_value(cell.strip()) for cell in row]
        if len(values) < size:
            values.extend([""] * (size - len(values)))
        return values[:size]

    def _coerce_value(self, value: str) -> Any:
        if value == "":
            return ""
        normalized = value.replace(",", ".")
        try:
            number = float(normalized)
        except ValueError:
            return value
        if number.is_integer():
            return int(number)
        return number
