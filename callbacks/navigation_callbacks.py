from dash import Input, Output, State, callback

from layouts.home_layout import create_home_layout
from layouts.stats_layout import create_stats_layout
from layouts.login_layout import create_login_layout

def register_navigation_callbacks(app):
    """
    Registra los callbacks de navegación para la aplicación
    
    Args:
        app (Dash): Instancia de la aplicación Dash
    """
    @app.callback(
        Output('page-content', 'children'),
        [Input('url', 'pathname')],
        [State('session-data', 'data')]
    )
    def display_page(pathname, session_data):
        """
        Maneja la navegación entre páginas basándose en la ruta y el estado de la sesión
        
        Args:
            pathname (str): Ruta actual
            session_data (dict): Datos de sesión
        
        Returns:
            Layout correspondiente a la ruta
        """
        # Si no hay sesión iniciada, mostrar login
        if not session_data or not session_data.get('authenticated'):
            return create_login_layout()
        
        # Manejar rutas
        if pathname == '/stats':
            return create_stats_layout()
        elif pathname == '/home':
            return create_home_layout()
        else:
            # Por defecto, mostrar login
            return create_login_layout()