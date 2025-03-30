from dash import html
import dash_bootstrap_components as dbc
from .base_layout import create_navbar
from utils.data_processing import load_data
import pandas as pd

def create_home_layout():
    """
    Crea el layout para la página de inicio (home)
    """
    navbar = create_navbar()
    
    return dbc.Container([
        navbar,
        html.H1("Dashboard Interactivo Alondras F.C.", className="text-center my-4"),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Sobre el Dashboard"),
                    dbc.CardBody([
                        html.P("Este dashboard te permite analizar los datos de analizados del equipo Alondras F.C."),
                        html.P("Utiliza la barra de navegación para acceder a las diferentes secciones:"),
                        html.Ul([
                            html.Li("Home: Información general y resumen del equipo"),
                            html.Li("Estadísticas: Análisis detallado de los partidos")
                        ])
                    ])
                ], className="mb-4"),
                dbc.Card([
                    dbc.CardHeader("Resumen del Equipo"),
                    dbc.CardBody(id="team-summary")
                ])
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Resumen por Jornada"),
                    dbc.CardBody(id="match-summary-table")
                ])
            ], width=6)
        ])
    ])