import pandas as pd
import re
from datetime import datetime
import os

from config import DATA_PATH

def extract_info_from_description(description):
    """
    Extrae información adicional de la columna Descripción
    
    Args:
        description (str): Cadena de descripción del partido
    
    Returns:
        dict: Información extraída del partido
    """
    match_info = {}
    
    try:
        # Formato esperado: J18_CONXO_0-4_ALONDRAS
        parts = description.split('_')
        
        # Extraer jornada (J18 -> 18)
        if len(parts) > 0 and parts[0].startswith('J'):
            match_info['jornada'] = int(parts[0][1:])
        
        # Extraer equipos
        if len(parts) > 1:
            match_info['equipo_local'] = parts[1]
        
        if len(parts) > 3:
            match_info['equipo_visitante'] = parts[3]
        
        # Extraer resultado
        if len(parts) > 2 and '-' in parts[2]:
            score_parts = parts[2].split('-')
            if len(score_parts) == 2:
                goles_local = int(score_parts[0])
                goles_visitante = int(score_parts[1])
                
                match_info['goles_local'] = goles_local
                match_info['goles_visitante'] = goles_visitante
                
                # Determinar resultado para Alondras
                if match_info.get('equipo_visitante') == 'ALONDRAS':
                    match_info['goles_favor'] = goles_visitante
                    match_info['goles_contra'] = goles_local
                    match_info['resultado'] = 'Victoria' if goles_visitante > goles_local else 'Derrota'
                    match_info['es_local'] = False
                    match_info['es_visitante'] = True
                elif match_info.get('equipo_local') == 'ALONDRAS':
                    match_info['goles_favor'] = goles_local
                    match_info['goles_contra'] = goles_visitante
                    match_info['resultado'] = 'Victoria' if goles_local > goles_visitante else 'Derrota'
                    match_info['es_local'] = True
                    match_info['es_visitante'] = False
                
                # Calcular puntos
                match_info['puntos'] = 3 if match_info.get('resultado') == 'Victoria' else 0
    
    except Exception as e:
        print(f"Error al procesar descripción '{description}': {e}")
    
    return match_info

def load_data():
    """
    Carga y procesa los datos desde el archivo Excel
    
    Returns:
        pd.DataFrame: Dataframe con datos procesados
    """
    try:
        # Verificar si el archivo existe
        if not os.path.exists(DATA_PATH):
            print(f"ERROR: El archivo no existe en la ruta {DATA_PATH}")
            print(f"Ruta absoluta: {os.path.abspath(DATA_PATH)}")
            raise FileNotFoundError(f"No se encuentra el archivo en {DATA_PATH}")
        
        # Información adicional del archivo
        print(f"Leyendo archivo: {DATA_PATH}")
        print(f"Tamaño del archivo: {os.path.getsize(DATA_PATH)} bytes")
        
        # Cargar el archivo Excel con información detallada
        df = pd.read_excel(DATA_PATH, engine='openpyxl')
        
        # Imprimir información del DataFrame
        print("Información del DataFrame:")
        print(f"Número de filas: {len(df)}")
        print(f"Columnas: {list(df.columns)}")
        
        # Convertir la columna de fecha a datetime si existe
        if 'Fecha' in df.columns:
            df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
        
        # Extraer información adicional de la columna Descripción
        if 'Descripción' in df.columns:
            # Obtener descripciones únicas 
            unique_descriptions = df['Descripción'].drop_duplicates().tolist()
            match_info_dict = {desc: extract_info_from_description(desc) for desc in unique_descriptions}
            
            # Agregar columnas extraídas al dataframe
            for col in ['jornada', 'equipo_local', 'equipo_visitante', 
                        'goles_local', 'goles_visitante', 'goles_favor', 
                        'goles_contra', 'resultado', 'es_local', 
                        'es_visitante', 'puntos']:
                df[col] = df['Descripción'].map(lambda x: match_info_dict.get(x, {}).get(col, None))
        
        return df
    
    except Exception as e:
        print(f"Error al cargar el archivo Excel: {e}")
        import traceback
        traceback.print_exc()
        raise