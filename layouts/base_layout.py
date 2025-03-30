from dash import html, dcc
import dash_bootstrap_components as dbc

def create_navbar():
    """
    Crea la barra de navegación para la aplicación
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
            dbc.Button("Salir", id="logout-button", color="danger", className="ml-auto")
        ]),
        color="dark",
        dark=True,
    )

def create_base_layout():
    """
    Crea el layout base que será común a todas las páginas autenticadas
    """
    navbar = create_navbar()
    
    return html.Div([
        navbar,
        html.Div(id="page-content-authenticated")
    ])