from excel_agent.parser import InformationParser


def test_parse_csv_information():
    spec = InformationParser().parse("Nombre,Edad\nAna,21\nLuis,30")

    assert spec.tables[0].headers == ["Nombre", "Edad"]
    assert spec.tables[0].rows == [["Ana", 21], ["Luis", 30]]


def test_parse_key_values():
    spec = InformationParser().parse("Cliente: ACME\nTotal: 120.5")

    assert spec.tables[0].title == "Resumen"
    assert spec.tables[0].rows == [["Cliente", "ACME"], ["Total", 120.5]]
