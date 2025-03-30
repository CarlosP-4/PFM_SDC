# Dashboard Alondras F.C.

## Descripción
Dashboard interactivo para análisis de datos del equipo Alondras F.C.

## Estructura del Proyecto
```
mi_proyecto/
│
├── assets/
│   └── logo_alondras.png
│
├── components/
│   ├── __init__.py
│   ├── navbar.py
│   └── login.py
│
├── data/
│   ├── __init__.py
│   ├── loader.py
│   └── preprocessing.py
│
├── layouts/
│   ├── __init__.py
│   ├── base_layout.py
│   ├── home_layout.py
│   ├── stats_layout.py
│   └── login_layout.py
│
├── callbacks/
│   ├── __init__.py
│   ├── navigation_callbacks.py
│   ├── login_callbacks.py
│   └── stats_callbacks.py
│
├── utils/
│   ├── __init__.py
│   ├── field_mapping.py
│   ├── pdf_generator.py
│   └── visualization.py
│
├── config.py
├── requirements.txt
└── app.py
```

## Requisitos
- Python 3.8+
- Dash
- Pandas
- Plotly
- Dash Bootstrap Components

## Instalación
1. Clonar el repositorio
2. Crear un entorno virtual
3. Instalar dependencias: `pip install -r requirements.txt`

## Ejecución
`python app.py`

## Características
- Análisis de partidos
- Visualización de estadísticas
- Exportación a PDF
- Filtrado avanzado de datos