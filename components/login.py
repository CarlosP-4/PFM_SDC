import dash_bootstrap_components as dbc
from dash import html

from config import ALONDRAS_AZUL, ALONDRAS_ROJO

def create_login_form():
    """
    Crea el formulario de login
    
    Returns:
        dbc.Card: Componente de formulario de login
    """
    return dbc.Card([
        dbc.CardHeader("Iniciar Sesión", className="text-center font-weight-bold", 
                      style={"backgroundColor": ALONDRAS_AZUL, "color": "white"}),
        dbc.CardBody([
            html.Div([
                html.I(className="fas fa-user", style={"color": ALONDRAS_AZUL}),
                html.Span(" Usuario:", className="ml-2")
            ], className="mb-2"),
            dbc.Input(id="input-username", placeholder="Usuario", type="text", className="mb-3"),
            
            html.Div([
                html.I(className="fas fa-lock", style={"color": ALONDRAS_AZUL}),
                html.Span(" Contraseña:", className="ml-2")
            ], className="mb-2"),
            dbc.Input(id="input-password", placeholder="Contraseña", type="password", className="mb-3"),
            
            dbc.Button("Entrar", id="login-button", color="primary", className="mt-3 w-100"),
            html.Div(id="login-alert")
        ], className="p-4")
    ], className="mx-auto shadow", style={"maxWidth": "400px", "border": f"1px solid {ALONDRAS_AZUL}"})