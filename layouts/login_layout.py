from dash import html
import dash_bootstrap_components as dbc

def create_login_layout(ALONDRAS_AZUL, ALONDRAS_ROJO):
    """
    Crea el layout de la página de login
    """
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Img(src="/assets/logo_alondras.png", height="120px", className="mb-4"),
                    html.H1("Dashboard Interactivo", className="text-center mb-1", 
                        style={"color": ALONDRAS_AZUL}),
                    html.H2("Alondras F.C.", className="text-center mb-4", 
                        style={"color": ALONDRAS_ROJO, "fontWeight": "bold"}),
                    html.Hr(),
                    dbc.Card([
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
                ], className="text-center")
            ], width=6, className="mx-auto")
        ], className="align-items-center min-vh-100")
    ], fluid=True, style={"backgroundImage": "linear-gradient(to bottom right, #f8f9fa, #e9ecef)"})