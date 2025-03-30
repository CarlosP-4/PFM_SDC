import pandas as pd

def evaluate_all_actions(zona_df):
    """
    Evalúa todas las acciones en el dataframe y las clasifica como correctas, incorrectas,
    o no evaluadas según criterios específicos más refinados.
    
    Args:
        zona_df (pd.DataFrame): Dataframe con acciones a evaluar
    
    Returns:
        dict: Diccionario con métricas de evaluación
    """
    correctos = 0
    incorrectos = 0
    no_evaluados = 0
    
    for _, row in zona_df.iterrows():
        if pd.notna(row['group']) and pd.notna(row['code']):
            group = str(row['group'])
            code = str(row['code'])
            
            # 1. Pase y Llegadas extremo area
            if code == "Pase" or code == "Llegadas extremo area" or "Llegadas extremo" in code:
                if "(C)" in group:
                    correctos += 1
                elif "(I)" in group:
                    incorrectos += 1
                elif "Correcto" in group or "correcto" in group:
                    correctos += 1
                elif "Incorrecto" in group or "incorrecto" in group or "perdida" in group.lower():
                    incorrectos += 1
                else:
                    # Buscar palabras clave para identificar éxitos
                    success_keywords = ["ocasión de gol", "con tiro", "con ataque", "Generar espacio", "Recibir Pase"]
                    failure_keywords = ["conlleva perdida", "fuera de juego"]
                    
                    if any(keyword in group for keyword in success_keywords):
                        correctos += 1
                    elif any(keyword in group for keyword in failure_keywords):
                        incorrectos += 1
                    else:
                        no_evaluados += 1
                        print(f"No se pudo evaluar: {code} - {group}")
            
            # 2. Transición ofensiva
            elif code == "Trans. Of" or "Trans. Of" in code:
                if "Sacado de zona" in group:
                    correctos += 1
                elif "Perdida" in group:
                    incorrectos += 1
                else:
                    no_evaluados += 1
                    print(f"No se pudo evaluar: {code} - {group}")
            
            # 3. Transición defensiva
            elif code == "Trans. Def" or "Trans. Def" in code:
                if "Robo" in group:
                    correctos += 1
                elif "No Robo" in group:
                    incorrectos += 1
                else:
                    no_evaluados += 1
                    print(f"No se pudo evaluar: {code} - {group}")
            
            # 4. Otros casos específicos
            elif "DFC" in code:
                if "(C)" in group:
                    correctos += 1
                elif "(I)" in group:
                    incorrectos += 1
                else:
                    no_evaluados += 1
                    print(f"No se pudo evaluar: {code} - {group}")
            
            elif "Centros" in code:
                if "(C)" in group:
                    correctos += 1
                elif "(I)" in group:
                    incorrectos += 1
                else:
                    no_evaluados += 1
                    print(f"No se pudo evaluar: {code} - {group}")
            
            elif "MC" in code:
                if "(C)" in group:
                    correctos += 1
                elif "(I)" in group:
                    incorrectos += 1
                else:
                    no_evaluados += 1
                    print(f"No se pudo evaluar: {code} - {group}")
            
            # 5. Caso general
            else:
                if "(C)" in group:
                    correctos += 1
                elif "(I)" in group:
                    incorrectos += 1
                elif "Correcto" in group or "correcto" in group:
                    correctos += 1
                elif "Incorrecto" in group or "incorrecto" in group:
                    incorrectos += 1
                else:
                    no_evaluados += 1
                    print(f"No se pudo evaluar: {code} - {group}")
    
    # Total evaluados excluyendo los no evaluados
    total_evaluados = correctos + incorrectos
    
    # Calcular efectividad solo basada en acciones evaluadas
    efectividad = (correctos / total_evaluados * 100) if total_evaluados > 0 else 0
    
    return {
        'total': len(zona_df),
        'correctos': correctos,
        'incorrectos': incorrectos,
        'no_evaluados': no_evaluados,
        'efectividad': efectividad,
        'total_evaluados': total_evaluados
    }