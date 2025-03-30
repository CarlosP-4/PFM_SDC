# Configuraciones globales del proyecto Alondras F.C. Dashboard

# Colores del club
ALONDRAS_AZUL = "#0047AB"  # Azul profundo
ALONDRAS_ROJO = "#E60026"  # Rojo intenso

# Rutas de archivos
DATA_PATH = r"C:\Users\carlo\OneDrive\Escritorio\Máster Python\Trabajo Fin de Máster (TFM)\Python_TFM\App_Dash\datoscombinados_liga_alondras.xlsx"

# Configuraciones de la aplicación
APP_CONFIG = {
    'suppress_callback_exceptions': True,
    'external_stylesheets': [
        'https://use.fontawesome.com/releases/v5.15.1/css/all.css'
    ]
}

# Credenciales de acceso (en un escenario real, esto debería estar en un lugar más seguro)
LOGIN_CREDENTIALS = {
    'username': 'admin',
    'password': 'admin'
}

# Configuraciones de visualización
VISUALIZATION_SETTINGS = {
    'campograma': {
        'width': 270,
        'height': 170
    },
    'default_periods': [1, 2]
}