import pandas as pd
import numpy as np
import os
from io import BytesIO
from fpdf import FPDF

def load_data():
    """
    Carga los datos desde el archivo Excel
    """
    try:
        # Usar la ruta absoluta al archivo Excel
        file_path = r"C:\Users\carlo\OneDrive\Escritorio\Máster Python\Trabajo Fin de Máster (TFM)\Python_TFM\App_Dash\datoscombinados_liga_alondras.xlsx"
        
        print(f"Intentando cargar el archivo desde: {file_path}")
        df = pd.read_excel(file_path)
        print(f"Archivo cargado exitosamente. Filas: {len(df)}, Columnas: {len(df.columns)}")
        print(f"Columnas en el archivo: {df.columns.tolist()}")
        
        # Convertir la columna de fecha a formato datetime si existe
        if 'Fecha' in df.columns:
            df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
        
        # Extraer información adicional de la columna Descripción
        if 'Descripción' in df.columns:
            # Obtener descripciones únicas 
            unique_descriptions = df['Descripción'].drop_duplicates().tolist()
            match_info_dict = {desc: extract_info_from_description(desc) for desc in unique_descriptions if pd.notna(desc)}
            
            # Agregar columnas extraídas al dataframe
            for col in ['jornada', 'equipo_local', 'equipo_visitante', 'goles_local', 'goles_visitante', 
                        'goles_favor', 'goles_contra', 'resultado', 'es_local', 'es_visitante', 'puntos']:
                df[col] = df['Descripción'].map(lambda x: match_info_dict.get(x, {}).get(col, None) if pd.notna(x) else None)
        
        return df
    
    except Exception as e:
        print(f"Error al cargar el archivo Excel: {e}")
        import traceback
        traceback.print_exc()
        return pd.DataFrame()  # Devolver un DataFrame vacío en caso de error

def extract_info_from_description(description):
    """
    Extrae información del campo Descripción
    Formato: J18_CONXO_0-4_ALONDRAS
    """
    match_info = {}
    
    try:
        # Separar los componentes
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
                if 'equipo_local' in match_info and 'equipo_visitante' in match_info:
                    if match_info['equipo_visitante'] == 'ALONDRAS':
                        match_info['goles_favor'] = goles_visitante
                        match_info['goles_contra'] = goles_local
                        if goles_visitante > goles_local:
                            match_info['resultado'] = 'Victoria'
                        else:
                            match_info['resultado'] = 'Derrota'
                        match_info['es_local'] = False
                        match_info['es_visitante'] = True
                    elif match_info['equipo_local'] == 'ALONDRAS':
                        match_info['goles_favor'] = goles_local
                        match_info['goles_contra'] = goles_visitante
                        if goles_local > goles_visitante:
                            match_info['resultado'] = 'Victoria'
                        else:
                            match_info['resultado'] = 'Derrota'
                        match_info['es_local'] = True
                        match_info['es_visitante'] = False
                    
                    # Calcular los puntos
                    match_info['puntos'] = 3 if match_info['resultado'] == 'Victoria' else 0
    except Exception as e:
        print(f"Error al procesar descripción '{description}': {e}")
    
    return match_info

def create_pdf(filtered_data):
    """
    Crea un PDF con la información del dataframe filtrado
    """
    # Verificaciones iniciales
    if filtered_data is None or len(filtered_data) == 0:
        print("Advertencia: Dataframe vacío o None")
        return None
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Título
    pdf.cell(0, 10, "Informe Detallado Alondras F.C.", ln=True, align='C')
    pdf.ln(10)
    
    # Información general
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"Total de registros: {len(filtered_data)}", ln=True)
    pdf.ln(5)
    
    # Columnas para mostrar
    columnas_principales = ['Descripción', 'Periodo', 'code', 'group', 'Player']
    
    # Encabezados
    pdf.set_font("Arial", 'B', 10)
    for col in columnas_principales:
        pdf.cell(40, 10, col, border=1)
    pdf.ln()
    
    # Datos
    pdf.set_font("Arial", size=8)
    for _, row in filtered_data.head(30).iterrows():
        for col in columnas_principales:
            if col in row.index:
                valor = str(row[col]) if pd.notna(row[col]) else '-'
                # Truncar valores largos
                valor = (valor[:20] + '...') if len(valor) > 20 else valor
                pdf.cell(40, 7, valor, border=1)
        pdf.ln()
    
    # Guardar en BytesIO
    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    
    return pdf_output