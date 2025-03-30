import dash_bootstrap_components as dbc
from dash import html

from config import ALONDRAS_AZUL

def create_navbar():
    """
    Crea la barra de navegación para la aplicación
    
    Returns:
        dbc.Navbar: Componente de barra de navegación
    """
    return dbc.Navbar(
        dbc.Container([
            # Logo y Nombre
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="/assets/logo_alondras.png", height="30px")),
                        dbc.Col(dbc.NavbarBrand("Alondras F.C.", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="/home",
                style={"textDecoration": "none"},
            ),
            
            # Menú de navegación
            dbc.Nav([
                dbc.NavItem(dbc.NavLink("Home", href="/home")),
                dbc.NavItem(dbc.NavLink("Estadísticas", href="/stats")),
            ], className="mr-auto", navbar=True),
            
            # Botón de salida
            dbc.Button("Salir", id="logout-button", color="danger", className="ml-auto")
        ]),
        color="dark",
        dark=True,
    )