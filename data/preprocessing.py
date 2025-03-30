import pandas as pd
import numpy as np

def normalize_coordinates(df):
    """
    Normaliza las coordenadas para asegurar que están en el rango 0-100
    
    Args:
        df (pd.DataFrame): Dataframe con columnas de coordenadas
    
    Returns:
        pd.DataFrame: Dataframe con coordenadas normalizadas
    """
    # Columnas de coordenadas a normalizar
    coord_columns = ['startX', 'startY', 'endX', 'endY']
    
    # Verificar si las columnas existen
    existing_columns = [col for col in coord_columns if col in df.columns]
    
    if not existing_columns:
        return df
    
    # Detectar el rango actual (valores máximos)
    max_x = max(df[['startX', 'endX']].max())
    max_y = max(df[['startY', 'endY']].max())
    
    # Dimensiones originales del campo
    ORIGINAL_WIDTH = 270
    ORIGINAL_HEIGHT = 170
    
    # Normalizar coordenadas
    for col in existing_columns:
        if 'X' in col:
            # Normalizar X (0-100)
            df[col] = (df[col] / ORIGINAL_WIDTH) * 100
        else:
            # Normalizar Y, invirtiendo el eje (0-100)
            df[col] = 100 - ((df[col] / ORIGINAL_HEIGHT) * 100)
        
        # Asegurar que estén en rango 0-100
        df[col] = df[col].clip(0, 100)
    
    return df

def assign_vertical_zones(df):
    """
    Asigna zonas verticales basadas en la posición X
    
    Args:
        df (pd.DataFrame): Dataframe con coordenadas normalizadas
    
    Returns:
        pd.DataFrame: Dataframe con zona vertical añadida
    """
    if 'startX' not in df.columns:
        return df
    
    # Definir zonas basadas en coordenadas X normalizadas
    def get_vertical_zone(x):
        if x < 25:
            return "Zona Defensiva"
        elif x < 50:
            return "Zona Pre-Defensiva"
        elif x < 75:
            return "Zona Pre-Ofensiva"
        else:
            return "Zona Ofensiva"
    
    # Añadir columna de zona vertical
    df['zona_vertical'] = df['startX'].apply(get_vertical_zone)
    
    return df

def assign_horizontal_zones(df):
    """
    Asigna pasillos horizontales basados en la posición Y
    
    Args:
        df (pd.DataFrame): Dataframe con coordenadas normalizadas
    
    Returns:
        pd.DataFrame: Dataframe con pasillo añadido
    """
    if 'startY' not in df.columns:
        return df
    
    # Definir pasillos basados en coordenadas Y normalizadas
    def get_horizontal_zone(y):
        if y < 25 or y >= 75:
            return "Pasillo Lateral"
        else:
            return "Pasillo Central"
    
    # Añadir columna de pasillo
    df['pasillo'] = df['startY'].apply(get_horizontal_zone)
    
    return df

def preprocess_data(df):
    """
    Función principal de preprocesamiento
    
    Args:
        df (pd.DataFrame): Dataframe original
    
    Returns:
        pd.DataFrame: Dataframe preprocesado
    """
    # Aplicar funciones de preprocesamiento en orden
    df = normalize_coordinates(df)
    df = assign_vertical_zones(df)
    df = assign_horizontal_zones(df)
    
    return df