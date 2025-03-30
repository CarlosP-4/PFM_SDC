from dash import html, dcc
import dash_bootstrap_components as dbc
from .base_layout import create_navbar

def create_stats_layout():
    """
    Crea el layout para la página de estadísticas
    """
    navbar = create_navbar()
    
    return dbc.Container([
        navbar,
        html.H1("Análisis Estadístico Alondras F.C.", className="text-center my-4"),
        
        # Filtros en una fila horizontal para ahorrar espacio vertical
        dbc.Card([
            dbc.CardHeader("Filtros de Análisis"),
            dbc.CardBody([
                dbc.Row([
                    # Filtro de jornada
                    dbc.Col([
                        html.Label("Jornada:"),
                        dcc.Dropdown(
                            id='jornada-dropdown',
                            placeholder="Seleccionar jornada",
                            className="mb-2"
                        ),
                    ], width=3),
                    
                    # Filtro de periodo
                    dbc.Col([
                        html.Label("Periodo:"),
                        dbc.Checklist(
                            id='period-check',
                            options=[
                                {"label": "1º Tiempo", "value": 1},
                                {"label": "2º Tiempo", "value": 2}
                            ],
                            value=[1, 2],
                            inline=True,
                            className="mb-2"
                        ),
                    ], width=2),
                    
                    # Filtro de categoría (code)
                    dbc.Col([
                        html.Label("Categoría:"),
                        dcc.Dropdown(
                            id='category-dropdown',
                            placeholder="Seleccionar categoría",
                            className="mb-2"
                        ),
                    ], width=3),
                    
                    # Filtro de grupo
                    dbc.Col([
                        html.Label("Grupo:"),
                        dcc.Dropdown(
                            id='group-dropdown',
                            placeholder="Seleccionar grupo",
                            className="mb-2"
                        ),
                    ], width=4),
                ]),
                
                # Botones de acción
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Aplicar Filtros", id="apply-filters", color="primary", className="w-100")
                    ], width=6),
                    dbc.Col([
                        dbc.Button("Exportar a PDF", id="export-pdf", color="success", className="w-100")
                    ], width=6),
                ], className="mt-3"),
            ])
        ], className="mb-4"),
        
        dbc.Row([
            # Campograma ocupa todo el ancho
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Campograma Interactivo"),
                    dbc.CardBody([
                        dcc.Graph(id="campograma-plot", style={"height": "600px"})
                    ])
                ], className="shadow-sm h-100")
            ], width=12),
        ]),

        # Nueva fila para distribución por tipo (ahora arriba de distribución por zonas)
        dbc.Row([
            # Distribución por tipo a ancho completo
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Distribución por Tipo"),
                    dbc.CardBody([
                        dcc.Graph(
                            id="group-distribution", 
                            style={
                                "height": "600px",
                                "width": "100%",
                                "backgroundColor": "white",
                                "padding": "0px",
                                "margin": "0px"
                            },
                            config={'displayModeBar': False}
                        )
                    ], style={"padding": "0", "backgroundColor": "white"})
                ], className="mb-3 shadow-sm")
            ], width=12),
        ]),

        # Distribución por zonas ahora va después y a ancho completo
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Distribución por Zonas"),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H6("Zonas Verticales", className="text-center"),
                                    html.Div(id="zona-vertical-stats")
                                ])
                            ], width=6),
                            dbc.Col([
                                html.Div([
                                    html.H6("Pasillos", className="text-center"),
                                    html.Div(id="pasillo-stats")
                                ])
                            ], width=6)
                        ])
                    ])
                ], className="mb-3 shadow-sm")
            ], width=12),
        ]),

        dbc.Row([
            # Tabla de datos detallados ocupa todo el ancho
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Datos Detallados"),
                    dbc.CardBody([
                        html.Div(id="filtered-data-detail", style={"max-height": "400px", "overflow-y": "auto"})
                    ])
                ], className="shadow-sm")
            ], width=12)
        ]),
        
        # Elementos para gestionar el "Ver más datos"
        dbc.Collapse(
            id="collapsed-data",
            is_open=False
        ),
        
        html.Div([
            dbc.Button(
                [html.I(className="fas fa-chevron-down mr-2"), "Ver todos los datos"],
                id="ver-mas-datos", 
                color="primary", 
                size="sm", 
                className="mt-2"
            )
        ], className="text-right"),
        
        # Componente para descargar PDF
        dcc.Download(id="download-pdf"),
        
        # Stores para datos de sesión y datos filtrados
        dcc.Store(id='filtered-data', storage_type='memory')
        
    ], fluid=True)  # Container más ancho para mejor aprovechamiento