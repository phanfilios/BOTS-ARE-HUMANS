# Excel Agent

Este es la vercion 1.1.1 del sistema de  bots execel se busca crear un agente de IA semejante a chat gpt codex que en ves de crear codigo este bot crea tablas de execel y libros de excel demanera detallada en base a informavion en tiempo real 

## Que hace ahora

- Recibe informacion como CSV, tabla Markdown, pares `campo: valor` o texto libre.
- Normaliza esa informacion en una especificacion interna.
- Crea un archivo `.xlsx` con hoja de resumen, tabla con estilo, filtros y columnas ajustadas.
- Emite eventos de progreso para que una UI pueda mostrar la creacion en tiempo real.

  <img width="954" height="722" alt="image" src="https://github.com/user-attachments/assets/ce910eb1-5e8a-44bd-b697-532676ea2442" />


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

## Vision

La arquitectura separa tres responsabilidades para crecer sin caos:

- Entrada inteligente: despues se puede conectar un modelo de IA para entender instrucciones mas complejas.
- Generacion de Excel: aqui vive el formato, formulas, estilos, graficos y multiples hojas.
- Experiencia en tiempo real: los eventos del agente estan listos para alimentar una UI tipo chat/agente.
