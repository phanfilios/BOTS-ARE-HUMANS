
# Excel Agent

Sistema local para convertir informacion en libros de Excel de forma visible,
paso a paso, como una base para un futuro agente con interfaz elegante y
minimalista.

<img width="718" height="491" alt="image" src="https://github.com/user-attachments/assets/ba4210a3-3bc3-48e5-87a3-3512762a3632" />


## Que hace ahora

- Recibe informacion como CSV, tabla Markdown, pares `campo: valor` o texto libre.
- Normaliza esa informacion en una especificacion interna.
- Crea un archivo `.xlsx` con hoja de resumen, tabla con estilo, filtros y columnas ajustadas.
- Detecta reportes de ventas con `Producto`, `Cantidad` y `Precio`.
- Calcula la columna `Total`, agrega `Total general` y crea un grafico por producto.
- Emite eventos de progreso para que una UI pueda mostrar la creacion en tiempo real.

## Estructura

```text
src/excel_agent/
  agent.py      Orquesta el flujo y emite eventos.
  parser.py     Convierte texto en tablas.
  builder.py    Genera el archivo Excel.
  cli.py        Interfaz de consola.
  models.py     Modelos compartidos.
examples/
  ventas.csv
  ventas_v2.csv
tests/
```

## Instalacion

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

## Uso rapido

Desde un archivo:

```bash
excel-agent -i examples/ventas.csv -o outputs/ventas.xlsx -t "Reporte de ventas"
```

Pegando informacion:

```bash
excel-agent -o outputs/reporte.xlsx
```

Tambien puedes ejecutarlo sin instalar el comando:

```bash
python -m excel_agent.cli -i examples/ventas.csv -o outputs/ventas.xlsx
```

## Ejemplo v2: ventas

```bash
python -m excel_agent.cli -i examples/ventas_v2.csv -o outputs/ventas_v2.xlsx -t "Reporte de ventas v2"
```

Si el archivo tiene estas columnas:

```csv
Producto,Cantidad,Precio
Teclado,12,35.5
Mouse,18,19.9
Monitor,5,149.99
```

El agente crea:

- Hoja `Ventas`.
- Columna `Total` con formulas como `=B2*C2`.
- Fila `Total general` con `=SUM(...)`.
- Grafico de barras por producto.

## Vision

La arquitectura separa tres responsabilidades para crecer sin caos:

- Entrada inteligente: despues se puede conectar un modelo de IA para entender instrucciones mas complejas.
- Generacion de Excel: aqui vive el formato, formulas, estilos, graficos y multiples hojas.
- Experiencia en tiempo real: los eventos del agente estan listos para alimentar una UI tipo chat/agente.
