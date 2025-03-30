import dash
from dash import Input, Output, State, callback
import dash_bootstrap_components as dbc

from config import LOGIN_CREDENTIALS

def register_login_callbacks(app):
    """
    Registra los callbacks relacionados con el inicio de sesión
    
    Args:
        app (Dash): Instancia de la aplicación Dash
    """
    @app.callback(
        [Output('session-data', 'data'),
         Output('login-alert', 'children'),
         Output('url', 'pathname')],
        [Input('login-button', 'n_clicks')],
        [State('input-username', 'value'),
         State('input-password', 'value')],
        prevent_initial_call=True
    )
    def login(n_clicks, username, password):
        """
        Maneja el proceso de inicio de sesión
        
        Args:
            n_clicks (int): Número de clics en el botón de login
            username (str): Nombre de usuario ingresado
            password (str): Contraseña ingresada
        
        Returns:
            tuple: Datos de sesión, alerta de login, ruta de navegación
        """
        if n_clicks is None:
            return dash.no_update, dash.no_update, dash.no_update
        
        # Verificar credenciales
        if (username == LOGIN_CREDENTIALS['username'] and 
            password == LOGIN_CREDENTIALS['password']):
            return {'authenticated': True}, None, '/home'
        else:
            return None, dbc.Alert(
                "Usuario o contraseña incorrectos", 
                color="danger", 
                className="mt-3"
            ), dash.no_update

    @app.callback(
        [Output('session-data', 'clear_data'),
         Output('url', 'pathname', allow_duplicate=True)],
        [Input('logout-button', 'n_clicks')],
        prevent_initial_call=True
    )
    def logout(n_clicks):
        """
        Maneja el proceso de cierre de sesión
        
        Args:
            n_clicks (int): Número de clics en el botón de logout
        
        Returns:
            tuple: Limpiar datos de sesión, ruta de navegación
        """
        if n_clicks is None:
            return dash.no_update, dash.no_update
        return True, '/'