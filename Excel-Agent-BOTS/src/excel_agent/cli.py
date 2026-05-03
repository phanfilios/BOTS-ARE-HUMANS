from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .agent import ExcelAgent


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Crea un archivo Excel desde informacion en texto.")
    parser.add_argument("-i", "--input", type=Path, help="Archivo .txt/.csv/.md con la informacion de entrada.")
    parser.add_argument("-o", "--output", type=Path, default=Path("outputs/reporte.xlsx"), help="Ruta del .xlsx final.")
    parser.add_argument("-t", "--title", default="Reporte generado", help="Titulo del libro.")
    args = parser.parse_args(argv)

    information = _read_information(args.input)
    agent = ExcelAgent()

    for event in agent.create_workbook(information, args.output, title=args.title):
        percent = int(event.progress * 100)
        print(f"[{percent:3d}%] {event.stage}: {event.message}")

    return 0


def _read_information(input_path: Path | None) -> str:
    if input_path:
        return input_path.read_text(encoding="utf-8")

    if not sys.stdin.isatty():
        return sys.stdin.read()

    print("Pega la informacion para convertirla en Excel. Termina con una linea vacia.")
    lines: list[str] = []
    while True:
        line = input("> ")
        if not line:
            break
        lines.append(line)
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
