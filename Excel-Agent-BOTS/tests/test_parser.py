from excel_agent.parser import InformationParser


def test_parse_csv_information():
    spec = InformationParser().parse("Nombre,Edad\nAna,21\nLuis,30")

    assert spec.tables[0].headers == ["Nombre", "Edad"]
    assert spec.tables[0].rows == [["Ana", 21], ["Luis", 30]]


def test_parse_key_values():
    spec = InformationParser().parse("Cliente: ACME\nTotal: 120.5")

    assert spec.tables[0].title == "Resumen"
    assert spec.tables[0].rows == [["Cliente", "ACME"], ["Total", 120.5]]


def test_parse_sales_table_adds_total_column():
    spec = InformationParser().parse("Producto,Cantidad,Precio\nTeclado,2,10\nMouse,3,5")

    table = spec.tables[0]
    assert table.title == "Ventas"
    assert table.headers == ["Producto", "Cantidad", "Precio", "Total"]
    assert table.rows == [["Teclado", 2, 10, 20], ["Mouse", 3, 5, 15]]
    assert table.metadata["chart"] == "product_total"


def test_parse_sales_instruction_creates_template():
    spec = InformationParser().parse(
        "Quiero una tabla de ventas con producto, cantidad, precio, total, total general y grafico por producto."
    )

    table = spec.tables[0]
    assert table.title == "Ventas"
    assert table.headers == ["Producto", "Cantidad", "Precio", "Total"]
    assert table.row_count == 5
    assert table.metadata["template"] is True
