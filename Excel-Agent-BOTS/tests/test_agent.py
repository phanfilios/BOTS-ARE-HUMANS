from excel_agent.agent import ExcelAgent


def test_agent_streams_done_event(tmp_path):
    output = tmp_path / "reporte.xlsx"
    events = list(ExcelAgent().create_workbook("A,B\n1,2", output))

    assert events[-1].stage == "done"
    assert output.exists()
