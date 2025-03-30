import pandas as pd

def assign_zones_by_pass_direction(filtered_df_normalized):
    """
    Asigna zonas verticales analizando la dirección de los pases
    
    Args:
        filtered_df_normalized (pd.DataFrame): Dataframe con coordenadas normalizadas
    
    Returns:
        pd.DataFrame: Dataframe con zonas verticales asignadas
    """
    # Crear una copia del dataframe
    df = filtered_df_normalized.copy()
    
    # Verificar columnas necesarias
    if 'startX' not in df.columns:
        print("Error: No se encontró la columna 'startX'")
        return df
    
    # Si no hay periodo, añadir valor predeterminado
    if 'Periodo' not in df.columns:
        df['Periodo'] = 1
    
    # Inicializar columna de zona_vertical
    df['zona_vertical'] = None
    
    # Procesar zonas para el primer periodo
    p1_mask = df['Periodo'] == 1
    if p1_mask.any():
        df.loc[p1_mask, 'zona_vertical'] = df.loc[p1_mask].apply(
            lambda row: "Zona Defensiva" if row["startX"] < 25 else 
                       "Zona Pre-Defensiva" if row["startX"] < 50 else
                       "Zona Pre-Ofensiva" if row["startX"] < 75 else
                       "Zona Ofensiva", 
            axis=1
        )
    
    # Procesar zonas para el segundo periodo (invertir dirección)
    p2_mask = df['Periodo'] == 2
    if p2_mask.any():
        df.loc[p2_mask, 'zona_vertical'] = df.loc[p2_mask].apply(
            lambda row: "Zona Ofensiva" if row["startX"] < 25 else 
                       "Zona Pre-Ofensiva" if row["startX"] < 50 else
                       "Zona Pre-Defensiva" if row["startX"] < 75 else
                       "Zona Defensiva", 
            axis=1
        )
    
    # Verificar si hay filas sin zona asignada
    missing_mask = df['zona_vertical'].isna()
    if missing_mask.any():
        print(f"ADVERTENCIA: {missing_mask.sum()} filas sin zona asignada")
        df.loc[missing_mask, 'zona_vertical'] = df.loc[missing_mask].apply(
            lambda row: "Zona Defensiva" if row["startX"] < 25 else 
                      "Zona Pre-Defensiva" if row["startX"] < 50 else
                      "Zona Pre-Ofensiva" if row["startX"] < 75 else
                      "Zona Ofensiva", 
            axis=1
        )
    
    return df