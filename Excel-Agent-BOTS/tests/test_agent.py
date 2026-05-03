from excel_agent.agent import ExcelAgent
from openpyxl import load_workbook


def test_agent_streams_done_event(tmp_path):
    output = tmp_path / "reporte.xlsx"
    events = list(ExcelAgent().create_workbook("A,B\n1,2", output))

    assert events[-1].stage == "done"
    assert output.exists()


def test_agent_builds_sales_workbook_with_formula_and_chart(tmp_path):
    output = tmp_path / "ventas.xlsx"
    list(ExcelAgent().create_workbook("Producto,Cantidad,Precio\nTeclado,2,10", output))

    workbook = load_workbook(output, data_only=False)
    sheet = workbook["Ventas"]

    assert sheet["D2"].value == "=B2*C2"
    assert sheet["C3"].value == "Total general"
    assert sheet["D3"].value == "=SUM(D2:D2)"
    assert len(sheet._charts) == 1
