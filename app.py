import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import os

# Importar layouts
from layouts.base_layout import create_navbar
from layouts.login_layout import create_login_layout
from layouts.home_layout import create_home_layout
from layouts.stats_layout import create_stats_layout

# Importar callbacks
from callbacks.stats_callbacks import register_stats_callbacks
from callbacks.home_callbacks import register_home_callbacks

# Definir los colores del club
ALONDRAS_AZUL = "#0047AB"  # Azul profundo
ALONDRAS_ROJO = "#E60026"  # Rojo intenso

# Inicializar la aplicación
app = dash.Dash(
    __name__, 
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        'https://use.fontawesome.com/releases/v5.15.1/css/all.css' 
    ],
    suppress_callback_exceptions=True
)

# Agregar estilos personalizados CSS
app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Dashboard Alondras F.C.</title>
        {%favicon%}
        {%css%}
        <style>
            /* Estilos personalizados con los colores del club */
            .navbar-dark {
                background-color: """ + ALONDRAS_AZUL + """ !important;
            }
            .btn-primary {
                background-color: """ + ALONDRAS_AZUL + """ !important;
                border-color: """ + ALONDRAS_AZUL + """ !important;
            }
            .btn-success {
                background-color: """ + ALONDRAS_ROJO + """ !important;
                border-color: """ + ALONDRAS_ROJO + """ !important;
            }
            .text-success {
                color: """ + ALONDRAS_ROJO + """ !important;
            }
            .bg-success, .progress-bar-success {
                background-color: """ + ALONDRAS_ROJO + """ !important;
            }
            .card-victoria {
                border-left: 5px solid """ + ALONDRAS_ROJO + """ !important;
            }
            .card-derrota {
                border-left: 5px solid #dc3545 !important;
            }
            .icon-victoria {
                color: """ + ALONDRAS_ROJO + """ !important;
            }
            .icon-trofeo {
                color: """ + ALONDRAS_ROJO + """ !important;
            }
            .icon-info {
                color: """ + ALONDRAS_AZUL + """ !important;
            }
            .icon-alondras {
                height: 30px;
                margin-right: 10px;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""

# Crear el login_layout
login_layout = create_login_layout(ALONDRAS_AZUL, ALONDRAS_ROJO)

# Diseño principal de la aplicación
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    # Almacenamiento de datos y estado de la sesión
    dcc.Store(id='session-data', storage_type='session'),
    dcc.Store(id='filtered-data', storage_type='memory')
])

# Callbacks básicos de navegación y login
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')],
    [State('session-data', 'data')]
)
def display_page(pathname, session_data):
    if not session_data or not session_data.get('authenticated'):
        return login_layout
        
    if pathname == '/stats':
        return create_stats_layout()  # Llamar a la función en lugar de usar stats_layout
    elif pathname == '/home':
        return create_home_layout()
    else:
        return login_layout

@app.callback(
    [Output('session-data', 'data'),
     Output('login-alert', 'children'),
     Output('url', 'pathname')],
    [Input('login-button', 'n_clicks')],
    [State('input-username', 'value'),
     State('input-password', 'value')]
)
def login(n_clicks, username, password):
    if n_clicks is None:
        return None, None, dash.no_update
    
    if username == 'admin' and password == 'admin':
        return {'authenticated': True}, None, '/home'
    else:
        return None, dbc.Alert("Usuario o contraseña incorrectos", color="danger", className="mt-3"), dash.no_update

@app.callback(
    [Output('session-data', 'clear_data'),
     Output('url', 'pathname', allow_duplicate=True)],
    [Input('logout-button', 'n_clicks')],
    prevent_initial_call=True
)
def logout(n_clicks):
    if n_clicks is None:
        return dash.no_update, dash.no_update
    return True, '/'

# Registrar callbacks específicos para cada página
register_stats_callbacks(app)
register_home_callbacks(app)

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)