from __future__ import annotations

from pathlib import Path

from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

from .models import WorkbookSpec


class ExcelWorkbookBuilder:
    def build(self, spec: WorkbookSpec, output_path: Path) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)

        workbook = Workbook()
        summary = workbook.active
        summary.title = "Resumen"
        self._write_summary(summary, spec)

        for table_spec in spec.tables:
            sheet = workbook.create_sheet(self._safe_sheet_name(table_spec.title))
            self._write_table(sheet, table_spec)

        workbook.save(output_path)
        return output_path

    def _write_summary(self, sheet, spec: WorkbookSpec) -> None:
        sheet["A1"] = spec.title
        sheet["A1"].font = Font(size=18, bold=True, color="1F2937")
        sheet["A3"] = "Tablas"
        sheet["A3"].font = Font(bold=True)
        sheet.append([])

        sheet["A4"] = "Nombre"
        sheet["B4"] = "Filas"
        sheet["C4"] = "Columnas"
        self._style_header(sheet, 4, 3)

        for table in spec.tables:
            sheet.append([table.title, table.row_count, table.column_count])

        self._autosize(sheet)

    def _write_table(self, sheet, table_spec) -> None:
        sheet.append(table_spec.headers)
        for row in table_spec.rows:
            sheet.append(row)

        self._apply_sales_formulas(sheet, table_spec)
        total_row = self._append_sales_total(sheet, table_spec)
        self._style_header(sheet, 1, table_spec.column_count)
        if total_row:
            self._style_total_row(sheet, total_row, table_spec.column_count)
        self._autosize(sheet)

        last_row = max(1, table_spec.row_count + 1)
        last_col = max(1, table_spec.column_count)
        ref = f"A1:{get_column_letter(last_col)}{last_row}"
        table = Table(displayName=self._safe_table_name(table_spec.title), ref=ref)
        table.tableStyleInfo = TableStyleInfo(
            name="TableStyleMedium2",
            showFirstColumn=False,
            showLastColumn=False,
            showRowStripes=True,
            showColumnStripes=False,
        )
        sheet.add_table(table)
        sheet.freeze_panes = "A2"
        self._add_sales_chart(sheet, table_spec)

    def _apply_sales_formulas(self, sheet, table_spec) -> None:
        if table_spec.metadata.get("kind") != "sales":
            return

        quantity_col = self._find_column(table_spec.headers, table_spec.metadata["quantity_header"])
        price_col = self._find_column(table_spec.headers, table_spec.metadata["price_header"])
        total_col = self._find_column(table_spec.headers, table_spec.metadata["total_header"])
        if not all([quantity_col, price_col, total_col]):
            return

        quantity_letter = get_column_letter(quantity_col)
        price_letter = get_column_letter(price_col)
        for row in range(2, table_spec.row_count + 2):
            sheet.cell(row=row, column=total_col).value = f"={quantity_letter}{row}*{price_letter}{row}"

    def _append_sales_total(self, sheet, table_spec) -> int | None:
        if table_spec.metadata.get("kind") != "sales" or table_spec.row_count == 0:
            return None

        total_col = self._find_column(table_spec.headers, table_spec.metadata["total_header"])
        if total_col is None:
            return None

        total_row = table_spec.row_count + 2
        label_col = max(1, total_col - 1)
        total_letter = get_column_letter(total_col)
        sheet.cell(row=total_row, column=label_col).value = "Total general"
        sheet.cell(row=total_row, column=total_col).value = f"=SUM({total_letter}2:{total_letter}{total_row - 1})"
        return total_row

    def _add_sales_chart(self, sheet, table_spec) -> None:
        if table_spec.metadata.get("chart") != "product_total" or table_spec.row_count == 0:
            return

        product_col = self._find_column(table_spec.headers, table_spec.metadata["product_header"])
        total_col = self._find_column(table_spec.headers, table_spec.metadata["total_header"])
        if product_col is None or total_col is None:
            return

        chart = BarChart()
        chart.title = "Ventas por producto"
        chart.y_axis.title = "Total"
        chart.x_axis.title = "Producto"
        chart.height = 7
        chart.width = 14

        data = Reference(sheet, min_col=total_col, min_row=1, max_row=table_spec.row_count + 1)
        categories = Reference(sheet, min_col=product_col, min_row=2, max_row=table_spec.row_count + 1)
        chart.add_data(data, titles_from_data=True)
        chart.set_categories(categories)
        sheet.add_chart(chart, f"{get_column_letter(table_spec.column_count + 2)}2")

    def _style_header(self, sheet, row: int, columns: int) -> None:
        fill = PatternFill("solid", fgColor="111827")
        for column in range(1, columns + 1):
            cell = sheet.cell(row=row, column=column)
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = fill
            cell.alignment = Alignment(horizontal="center")

    def _style_total_row(self, sheet, row: int, columns: int) -> None:
        fill = PatternFill("solid", fgColor="E5E7EB")
        for column in range(1, columns + 1):
            cell = sheet.cell(row=row, column=column)
            cell.font = Font(bold=True, color="111827")
            cell.fill = fill

    def _autosize(self, sheet) -> None:
        for column_cells in sheet.columns:
            max_length = 0
            column = get_column_letter(column_cells[0].column)
            for cell in column_cells:
                if cell.value is not None:
                    max_length = max(max_length, len(str(cell.value)))
            sheet.column_dimensions[column].width = min(max(max_length + 2, 12), 42)

    def _safe_sheet_name(self, name: str) -> str:
        safe = "".join(ch for ch in name if ch not in r"[]:*?/\\").strip()
        return (safe or "Tabla")[:31]

    def _safe_table_name(self, name: str) -> str:
        safe = "".join(ch if ch.isalnum() else "_" for ch in name).strip("_")
        safe = safe or "Tabla"
        if safe[0].isdigit():
            safe = f"T_{safe}"
        return safe[:255]

    def _find_column(self, headers: list[str], target: str) -> int | None:
        normalized_target = target.strip().lower()
        for index, header in enumerate(headers, start=1):
            if header.strip().lower() == normalized_target:
                return index
        return None
