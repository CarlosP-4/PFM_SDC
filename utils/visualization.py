import dash
from dash import html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dash import html
import dash_bootstrap_components as dbc

def create_improved_campograma(filtered_df_normalized, jornada=None, periods=None):
    """
    Crea un campograma mejorado con líneas más visibles
    """
    campo_fig = go.Figure()
    
    # Campo verde con un tono más claro para mejor contraste
    campo_fig.add_shape(
        type="rect", x0=0, y0=0, x1=100, y1=100,
        line=dict(color="white", width=2),  # Borde blanco más grueso
        fillcolor="rgba(144,238,144,0.5)"  # Verde claro más transparente
    )
    
    # Líneas verticales para zonas con mayor grosor y opacidad
    campo_fig.add_shape(
        type="line", x0=25, y0=0, x1=25, y1=100,
        line=dict(color="rgba(255,255,255,0.9)", width=1.5, dash="dash")  # Más grueso y opaco
    )
    campo_fig.add_shape(
        type="line", x0=50, y0=0, x1=50, y1=100,
        line=dict(color="rgba(255,255,255,0.9)", width=2)  # Línea central más gruesa
    )
    campo_fig.add_shape(
        type="line", x0=75, y0=0, x1=75, y1=100,
        line=dict(color="rgba(255,255,255,0.9)", width=1.5, dash="dash")  # Más grueso y opaco
    )
    
    # Líneas horizontales para pasillos con mayor grosor y opacidad
    campo_fig.add_shape(
        type="line", x0=0, y0=25, x1=100, y1=25,
        line=dict(color="rgba(255,255,255,0.9)", width=1.5, dash="dash")  # Más grueso y opaco
    )
    campo_fig.add_shape(
        type="line", x0=0, y0=75, x1=100, y1=75,
        line=dict(color="rgba(255,255,255,0.9)", width=1.5, dash="dash")  # Más grueso y opaco
    )
    
    # Áreas con líneas más gruesas y destacadas
    campo_fig.add_shape(  # Área izquierda
        type="rect", x0=0, y0=30, x1=16, y1=70,
        line=dict(color="rgba(255,255,255,1)", width=2.5),  # Mucho más grueso y totalmente opaco
        fillcolor="rgba(0,0,0,0)"
    )
    campo_fig.add_shape(  # Área derecha
        type="rect", x0=84, y0=30, x1=100, y1=70,
        line=dict(color="rgba(255,255,255,1)", width=2.5),  # Mucho más grueso y totalmente opaco
        fillcolor="rgba(0,0,0,0)"
    )
    
    # Círculo central más destacado
    campo_fig.add_shape(
        type="circle", xref="x", yref="y",
        x0=40, y0=40, x1=60, y1=60,
        line=dict(color="rgba(255,255,255,1)", width=2.5)  # Mucho más grueso y totalmente opaco
    )
    
    # Definir colores personalizados por categoría y grupo - Colores más saturados
    color_personalizado = {
        # Pases en largo - Azules más saturados (diferentes tonos)
        "Largo (C) ocasión de gol": "#000080",  # Azul marino
        "Largo (C) ocasión con centro": "#0000CD",  # Azul medio
        "Largo (C) con tiro frontal": "#0000FF",  # Azul puro
        "Largo (C) con ataque posicional": "#1E90FF",  # Dodger blue
        "Largo (C) con tiro de esquina": "#4169E1",  # Azul real
        "Largo (I) conlleva perdida": "#87CEEB",  # Azul cielo
        "Largo (I) fuera de juego": "#00BFFF",  # Azul profundo cielo
    
        # Categorías DFC - Morados más saturados
        "DFC campo rival (C)": "#4B0082",  # Índigo
        "DFC campo rival (I)": "#8A2BE2",  # Violeta azulado
    
        # Categorías Centros - Naranjas más saturados
        "Centros en llegada (C)": "#FF4500",  # Naranja-rojo
        "Centros en llegada (I)": "#FF8C00",  # Naranja oscuro
    
        # Categorías MC - Amarillos más saturados
        "MC (encara) (C)": "#FFD700",  # Oro
        "MC (encara) (I)": "#DAA520",  # Dorado
        
        # Llegadas extremo área (agregar diferentes colores)
        "Generar espacio (C)": "#06402B",  # Verde oscuro
        "Generar espacio (I)": "#00FF00",  # Verde
        "Recibir Pase (C)": "#7CFC00",  # Verde césped
        "Recibir Pase (I)": "#90EE90",  # Verde claro
    
        # Transiciones ofensivas (varios colores más intensos)
        "Perdida de balón": "#FF0000",  # Rojo puro
        "Sacado de zona- Corner": "#FF00FF",  # Magenta
        "Sacado de zona- Juego Pos": "#FFFF00",  # Amarillo brillante
        "Sacado de zona- Ocasión de gol": "#00FFFF",  # Cian
        "Sacado de zona- Ocasión remate": "#00FF00",  # Verde brillante

        # Transiciones defensivas (colores muy vivos y distintivos)
        "Robo": "#FF00FF",  # Magenta
        "No Robo": "#00FFFF",  # Cian
    }
    
    # Colores base para categorías no especificadas - Más saturados
    code_colors = {
        "Pase": "#FF0000",  # Rojo puro
        "Llegadas extremo area": "#00FF00",  # Verde puro
        "Trans. Def": "#8A2BE2",  # Violeta azulado
        "Trans. Of": "#FF8C00",  # Naranja oscuro
        "Centros en llegada": "#FF4500"  # Naranja-rojo
    }   
    
    # Dibujar flechas en el campo con líneas más gruesas
    if 'code' in filtered_df_normalized.columns and 'group' in filtered_df_normalized.columns:
        # Agrupar datos por grupo para la leyenda
        grouped_data = filtered_df_normalized.groupby('group')
    
        for group_name, group_data in grouped_data:
            # Asegurarse de que group_name sea string
            group_name_str = str(group_name)
            
            # Determinar si es una transición y de qué tipo
            es_transicion_of = False
            es_transicion_def = False
            if not group_data.empty and 'code' in group_data.columns:
                codigo = group_data['code'].iloc[0]
                if pd.notna(codigo):
                    es_transicion_of = "Trans. Of" in codigo
                    es_transicion_def = "Trans. Def" in codigo
            
            # Determinar color usando el diccionario personalizado
            color = color_personalizado.get(group_name_str, 
                    code_colors.get(group_data['code'].iloc[0] 
                                 if not group_data.empty else "Otro", "#333333"))
            
            if es_transicion_of or es_transicion_def:
                # Para transiciones, solo mostramos el punto inicial (sin flechas)
                x_values = []
                y_values = []
                
                for _, row in group_data.iterrows():
                    if pd.notna(row['startX']) and pd.notna(row['startY']):
                        x_values.append(row['startX'])
                        y_values.append(row['startY'])
                
                # Solo agregar el trace si hay puntos
                if x_values:
                    # Símbolo diferente para cada tipo de transición
                    symbol = 'diamond' if es_transicion_of else 'square'
                    
                    campo_fig.add_trace(
                        go.Scatter(
                            x=x_values,
                            y=y_values,
                            mode='markers',
                            marker=dict(
                                color=color, 
                                size=20,  # Puntos más grandes para transiciones
                                symbol=symbol,
                                line=dict(width=2, color='white')  # Borde blanco para destacar
                            ),
                            name=group_name_str,
                            legendgroup=group_name_str,
                            hoverinfo='name',
                            opacity=1.0  # Opacidad completa
                        )
                    )
            else:
                # Para el resto de acciones, crear flechas
                segments = []
                for _, row in group_data.iterrows():
                    if pd.notna(row['startX']) and pd.notna(row['startY']) and pd.notna(row['endX']) and pd.notna(row['endY']):
                        segments.append({
                            'x_start': row['startX'],
                            'y_start': row['startY'],
                            'x_end': row['endX'],
                            'y_end': row['endY']
                        })
                
                # Dibujar cada segmento como una flecha individual
                first_segment = True
                for segment in segments:
                    # Determinar si es una llegada de extremo para ajustar el grosor
                    es_llegada_extremo = False
                    if not group_data.empty and 'code' in group_data.columns:
                        codigo = group_data['code'].iloc[0]
                        if pd.notna(codigo):
                            es_llegada_extremo = "Llegadas extremo area" in codigo or "Legadas extremo area" in codigo
                    
                    # Ajustar grosor según el tipo
                    line_width = 4.5 if es_llegada_extremo else 3.5
                    marker_size = [12, 14] if es_llegada_extremo else [10, 12]
                    
                    campo_fig.add_trace(
                        go.Scatter(
                            x=[segment['x_start'], segment['x_end']],
                            y=[segment['y_start'], segment['y_end']],
                            mode='lines+markers',
                            line=dict(color=color, width=line_width),
                            marker=dict(
                                size=marker_size,
                                symbol=['circle', 'triangle-right'],
                                color=color,
                                line=dict(width=1.5 if es_llegada_extremo else 1, color='white' if es_llegada_extremo else 'rgba(0,0,0,0.5)')
                            ),
                            name=group_name_str,
                            legendgroup=group_name_str,
                            showlegend=first_segment,  # Solo la primera aparece en la leyenda
                            hoverinfo='name',
                            opacity=1.0 if es_llegada_extremo else 0.9  # Mayor opacidad para llegadas extremo
                        )
                    )
                    first_segment = False  # Después del primer segmento, no mostrar en leyenda

    # Configuración adicional optimizada
    jornada_info = jornada if jornada else "Todas las jornadas"
    periodos_text = ", ".join([f"Periodo {p}" for p in periods]) if periods else "Todos los periodos"
    
    campo_fig.update_layout(
        title={
            'text': f"Campograma - {jornada_info} ({periodos_text})",
            'font': {'size': 16}
        },
        legend={
            'title': {'text': 'Tipos de acciones', 'font': {'size': 14, 'color': '#333'}},
            'orientation': 'v',
            'yanchor': 'top',
            'y': 1,
            'xanchor': 'left',
            'x': 1.05,
            'font': {'size': 11},  # Fuente más grande en la leyenda
            'tracegroupgap': 8,  # Mayor separación entre grupos
            'bgcolor': 'rgba(255,255,255,0.9)',  # Fondo blanco semi-transparente
            'bordercolor': '#CCCCCC',
            'borderwidth': 1
        },
        xaxis=dict(range=[-5, 105], showgrid=False, zeroline=False, visible=False),
        yaxis=dict(range=[-5, 105], showgrid=False, zeroline=False, visible=False),
        height=600,  # Aumentar la altura para mejor visualización
        plot_bgcolor='rgba(144,238,144,0.5)',  # Fondo de campo más claro
        paper_bgcolor='white',
        margin=dict(l=10, r=10, t=50, b=10)
    )
    
    return campo_fig

def evaluate_all_actions(zona_df):
    """
    Evalúa todas las acciones en el dataframe y las clasifica como correctas, incorrectas,
    o no evaluadas según criterios específicos más refinados.
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
    
    # Imprimir un resumen para diagnóstico
    print(f"Resumen de evaluación: {correctos} correctos, {incorrectos} incorrectos, {no_evaluados} no evaluados")
    
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

# FUNCIÓN CRÍTICA PARA DIRECCIÓN DE ATAQUE: 
# Esta es la función que analiza la dirección de ataque y asigna zonas correctamente
def assign_zones_by_pass_direction(filtered_df_normalized):
    """
    Asigna zonas verticales analizando cada partido individualmente
    y manteniendo consistencia entre periodos.
    """
    # Configuración específica por jornada
    configuracion_jornadas = {
        'J23': {
            'periodo1': 'izquierda_a_derecha',
            'periodo2': 'derecha_a_izquierda'
        },
        'J21': {
            'periodo1': 'derecha_a_izquierda',
            'periodo2': 'izquierda_a_derecha'
        },
        'J19': {
            'periodo1': 'derecha_a_izquierda',
            'periodo2': 'izquierda_a_derecha'
        },
        'J18': {
            'periodo1': 'izquierda_a_derecha',
            'periodo2': 'derecha_a_izquierda'
        }
    }
    
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
    
    # Obtener jornada de la descripción
    jornada = None
    if 'Descripción' in df.columns and not df['Descripción'].empty:
        descripcion = df['Descripción'].iloc[0]
        partes = descripcion.split('_')
        if partes[0].startswith('J'):
            jornada = partes[0]
    
    def asignar_zonas(df, direccion):
        """
        Asigna zonas basándose en la dirección de ataque
        """
        if direccion == 'izquierda_a_derecha':
            return df.apply(
                lambda row: "Zona Defensiva" if row["startX"] < 25 else 
                           "Zona Pre-Defensiva" if row["startX"] < 50 else
                           "Zona Pre-Ofensiva" if row["startX"] < 75 else
                           "Zona Ofensiva", 
                axis=1
            )
        else:  # derecha_a_izquierda
            return df.apply(
                lambda row: "Zona Ofensiva" if row["startX"] < 25 else 
                           "Zona Pre-Ofensiva" if row["startX"] < 50 else
                           "Zona Pre-Defensiva" if row["startX"] < 75 else
                           "Zona Defensiva", 
                axis=1
            )
    
    # Verificar si tenemos configuración para esta jornada
    if jornada in configuracion_jornadas:
        config_jornada = configuracion_jornadas[jornada]
        
        # Procesamiento por periodos
        p1_mask = df['Periodo'] == 1
        p2_mask = df['Periodo'] == 2
        
        # Asignar zonas para periodo 1
        if p1_mask.any():
            df.loc[p1_mask, 'zona_vertical'] = asignar_zonas(
                df.loc[p1_mask], 
                config_jornada['periodo1']
            )
        
        # Asignar zonas para periodo 2
        if p2_mask.any():
            df.loc[p2_mask, 'zona_vertical'] = asignar_zonas(
                df.loc[p2_mask], 
                config_jornada['periodo2']
            )
    else:
        # Asignación por defecto si no hay configuración específica
        print(f"Advertencia: No hay configuración específica para la jornada {jornada}")
        df['zona_vertical'] = df.apply(
            lambda row: "Zona Defensiva" if row["startX"] < 25 else 
                      "Zona Pre-Defensiva" if row["startX"] < 50 else
                      "Zona Pre-Ofensiva" if row["startX"] < 75 else
                      "Zona Ofensiva", 
            axis=1
        )
    
    # Verificar si hay filas sin zona asignada
    missing_mask = df['zona_vertical'].isna()
    if missing_mask.any():
        print(f"ADVERTENCIA: {missing_mask.sum()} filas sin zona asignada")
        # Asignar zonas predeterminadas para las filas sin zona
        df.loc[missing_mask, 'zona_vertical'] = df.apply(
            lambda row: "Zona Defensiva" if row["startX"] < 25 else 
                      "Zona Pre-Defensiva" if row["startX"] < 50 else
                      "Zona Pre-Ofensiva" if row["startX"] < 75 else
                      "Zona Ofensiva", 
            axis=1
        )
    
    return df

def crear_efectividad_mejorada(correctas, incorrectas, no_evaluadas=0):
    """
    Crea una visualización de efectividad con un gráfico donut simple
    """
    total_evaluadas = correctas + incorrectas
    efectividad_porcentaje = (correctas / total_evaluadas * 100) if total_evaluadas > 0 else 0
    
    # Determinar color según efectividad
    if efectividad_porcentaje >= 80:
        color_efectividad = "#28a745"  # Verde para buena efectividad
    elif efectividad_porcentaje >= 60:
        color_efectividad = "#ffc107"  # Amarillo para efectividad media
    else:
        color_efectividad = "#dc3545"  # Rojo para efectividad baja
    
    return html.Div([
        # Gráfico donut con porcentaje en el centro
        html.Div([
            # Contenedor del donut
            html.Div(
                style={
                    "width": "120px",
                    "height": "120px",
                    "borderRadius": "50%",
                    "background": f"conic-gradient({color_efectividad} 0% {efectividad_porcentaje}%, #e9ecef {efectividad_porcentaje}% 100%)",
                    "display": "flex",
                    "alignItems": "center",
                    "justifyContent": "center",
                    "margin": "0 auto",
                    "position": "relative"
                },
                children=[
                    # Círculo interior blanco para crear efecto donut
                    html.Div(
                        style={
                            "width": "80px",
                            "height": "80px",
                            "borderRadius": "50%",
                            "background": "white",
                            "display": "flex",
                            "flexDirection": "column",
                            "alignItems": "center",
                            "justifyContent": "center"
                        },
                        children=[
                            # Porcentaje
                            html.Div(
                                f"{efectividad_porcentaje:.1f}%",
                                style={
                                    "fontSize": "20px",
                                    "fontWeight": "bold",
                                    "color": color_efectividad
                                }
                            ),
                            # Texto "Efectividad"
                            html.Div(
                                "Efectividad",
                                style={
                                    "fontSize": "10px",
                                    "color": "#6c757d"
                                }
                            )
                        ]
                    )
                ]
            )
        ], className="mb-4"),
        
        # Tarjetas para correctas e incorrectas
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-check-circle mr-2", style={"color": "#28a745"}),
                            "Correctas"
                        ], className="font-weight-bold"),
                        html.Div(f"{correctas}", style={"fontSize": "24px", "color": "#28a745", "textAlign": "center"})
                    ], className="text-center")
                ])
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-times-circle mr-2", style={"color": "#dc3545"}),
                            "Incorrectas"
                        ], className="font-weight-bold"),
                        html.Div(f"{incorrectas}", style={"fontSize": "24px", "color": "#dc3545", "textAlign": "center"})
                    ], className="text-center")
                ])
            ], width=6)
        ], className="mb-3"),
        
        # No evaluadas (si hay)
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-question-circle mr-2", style={"color": "#6c757d"}),
                            "No evaluadas"
                        ], className="font-weight-bold text-muted"),
                        html.Div(f"{no_evaluadas}", className="text-center text-muted", style={"fontSize": "18px"})
                    ], className="text-center")
                ])
            ], width=12)
        ]) if no_evaluadas > 0 else None
    ])

def crear_distribucion_categorias(filtered_df):
    """
    Crea una visualización mejorada para la distribución por categorías
    """
    distribucion_categoria = []
    if 'code' in filtered_df.columns:
        # Obtener los valores más frecuentes
        categorias = filtered_df['code'].value_counts().head(5)
        total = filtered_df.shape[0]
        
        # Mapeo de colores según el tipo de categoría
        color_map = {
            "Trans. Def.": "#4169E1",  # Azul real
            "Pase": "#1E90FF",         # Azul cielo
            "Trans. Of.": "#0047AB",   # Azul Alondras
            "Llegadas extremos area": "#1F75FE", # Azul cobalto
            "Centros en llegada": "#0000CD",   # Azul medio
            # Colores adicionales por si hay más categorías
            "DFC": "#00008B",          # Azul oscuro
            "MC": "#5D9CEC",           # Azul claro
        }
        
        for cat, count in categorias.items():
            porcentaje = (count / total) * 100
            
            # Determinar color basado en la categoría
            color = "#1E90FF"  # Color predeterminado azul
            for key in color_map:
                if key in cat:
                    color = color_map[key]
                    break
            
            distribucion_categoria.append(
                html.Div([
                    # Encabezado con porcentaje destacado
                    html.Div([
                        html.Span(f"{porcentaje:.1f}%", 
                                 className="font-weight-bold",
                                 style={"fontSize": "16px", "color": color}),
                        html.Span(f" - {count} registros", 
                                 className="text-muted small")
                    ], className="d-flex justify-content-between align-items-center mb-1"),
                    
                    # Barra de progreso con gradiente
                    html.Div([
                        html.Div(
                            style={
                                "width": f"{porcentaje}%",
                                "height": "24px",
                                "backgroundColor": color,
                                "borderRadius": "4px",
                                "display": "flex",
                                "alignItems": "center",
                                "paddingLeft": "10px"
                            },
                            children=html.Span(
                                cat,
                                style={
                                    "color": "white", 
                                    "fontWeight": "bold",
                                    "textShadow": "1px 1px 1px rgba(0,0,0,0.5)",
                                    "fontSize": "14px",
                                    "overflow": "hidden",
                                    "textOverflow": "ellipsis",
                                    "whiteSpace": "nowrap"
                                }
                            ) if porcentaje > 15 else None  # Solo mostrar texto si hay suficiente espacio
                        )
                    ], style={
                        "backgroundColor": "#f0f0f0",
                        "borderRadius": "4px",
                        "marginBottom": "15px",
                        "width": "100%"
                    })
                ])
            )
    else:
        distribucion_categoria = [html.P("No hay datos de categoría disponibles")]
    
    return html.Div(distribucion_categoria)

def crear_donut_efectividad(efectividad, tamaño=80):
    """
    Crea un gráfico donut para mostrar la efectividad
    
    Args:
        efectividad: Porcentaje de efectividad (0-100)
        tamaño: Tamaño del donut en píxeles
    """
    # Determinar color según efectividad
    if efectividad >= 80:
        color = "#28a745"  # Verde para buena efectividad
    elif efectividad >= 60:
        color = "#ffc107"  # Amarillo para efectividad media
    else:
        color = "#dc3545"  # Rojo para efectividad baja
    
    return html.Div(
        style={
            "width": f"{tamaño}px",
            "height": f"{tamaño}px",
            "borderRadius": "50%",
            "background": f"conic-gradient({color} 0% {efectividad}%, #e9ecef {efectividad}% 100%)",
            "display": "flex",
            "alignItems": "center",
            "justifyContent": "center",
            "margin": "0 auto",
        },
        children=[
            html.Div(
                style={
                    "width": f"{tamaño*0.7}px",
                    "height": f"{tamaño*0.7}px",
                    "borderRadius": "50%",
                    "background": "white",
                    "display": "flex",
                    "alignItems": "center",
                    "justifyContent": "center",
                },
                children=html.Div(
                    f"{efectividad:.1f}%",
                    style={
                        "fontWeight": "bold",
                        "color": color,
                        "fontSize": f"{tamaño*0.2}px"
                    }
                )
            )
        ]
    )

def crear_detalle_filtrado(filtered_df, jornada, periods, efectividad_general_content):
    """
    Crea un componente visual mejorado para mostrar el detalle de los datos filtrados.
    """
    # Verificar si hay datos para mostrar
    if filtered_df is None or len(filtered_df) == 0:
        return dbc.Alert(
            [
                html.I(className="fas fa-exclamation-circle mr-2"),
                "No hay datos disponibles con los filtros seleccionados."
            ], 
            color="warning",
            className="mb-0"
        )
    
    # Obtener distribución por categoría si existe la columna
    distribucion_categoria = []
    if 'code' in filtered_df.columns:
        # Obtener los valores más frecuentes
        categorias = filtered_df['code'].value_counts().head(5)
        total = filtered_df.shape[0]
        
        for cat, count in categorias.items():
            porcentaje = (count / total) * 100
            distribucion_categoria.append(
                html.Div([
                    dbc.Progress(
                        value=porcentaje,
                        color="primary",
                        striped=True,
                        className="mb-1",
                        style={"height": "20px"}
                    ),
                    html.Div([
                        html.Span(f"{cat} ({count} registros - {porcentaje:.1f}%)")
                    ], className="mt-1 mb-2")
                ])
            )
    else:
        distribucion_categoria = [html.P("No hay datos de categoría disponibles")]
    
    # Obtener información del rival y resultado si está disponible
    rival_info = ""
    resultado_info = ""
    if 'Descripción' in filtered_df.columns and filtered_df['Descripción'].notna().any():
        # Extraer rival y resultado de la descripción (formato: J18_CONXO_0-4_ALONDRAS)
        try:
            desc = filtered_df['Descripción'].iloc[0]
            partes = desc.split('_')
            if len(partes) >= 4:
                resultado = partes[2]  # El resultado está en la tercera parte (índice 2)
                
                if partes[1] == "ALONDRAS":
                    rival_info = partes[3]  # El rival es el equipo visitante
                    # Invertir el resultado para mostrar primero los goles de Alondras
                    goles = resultado.split('-')
                    if len(goles) == 2:
                        resultado_info = f"{goles[0]}-{goles[1]}"  # Alondras - Rival
                else:
                    rival_info = partes[1]  # El rival es el equipo local
                    # Invertir el resultado para mostrar primero los goles de Alondras
                    goles = resultado.split('-')
                    if len(goles) == 2:
                        resultado_info = f"{goles[1]}-{goles[0]}"  # Alondras - Rival
        except:
            rival_info = ""
            resultado_info = ""
    
    # Crear jugadores destacados con formato podio
    jugadores_destacados = html.Div()
    if 'Player' in filtered_df.columns:
        # Obtener top 3 jugadores
        top_players = filtered_df['Player'].value_counts().head(3)
        
        if len(top_players) > 0:
            # Crear diseño de podio
            jugadores_destacados = html.Div([
                dbc.Row([
                    # Segundo lugar (izquierda)
                    dbc.Col([
                        html.Div(className="podium-item position-second", style={
                            "height": "70px", 
                            "backgroundColor": "#A0A0A0", 
                            "display": "flex", 
                            "alignItems": "flex-end",
                            "justifyContent": "center",
                            "padding": "5px"
                        }),
                        html.Div([
                            html.Div(top_players.index[1] if len(top_players) > 1 else "", 
                                    className="font-weight-bold text-center"),
                            html.Div(f"{top_players.iloc[1] if len(top_players) > 1 else 0} acciones", 
                                    className="small text-center")
                        ])
                    ], width=4, className="text-center"),
                    
                    # Primer lugar (centro)
                    dbc.Col([
                        html.Div(className="podium-item position-first", style={
                            "height": "100px", 
                            "backgroundColor": "#FFD700", 
                            "display": "flex", 
                            "alignItems": "flex-end",
                            "justifyContent": "center",
                            "padding": "5px"
                        }),
                        html.Div([
                            html.Div(top_players.index[0] if len(top_players) > 0 else "", 
                                    className="font-weight-bold text-center"),
                            html.Div(f"{top_players.iloc[0] if len(top_players) > 0 else 0} acciones", 
                                    className="small text-center")
                        ])
                    ], width=4, className="text-center"),
                    
                    # Tercer lugar (derecha)
                    dbc.Col([
                        html.Div(className="podium-item position-third", style={
                            "height": "50px", 
                            "backgroundColor": "#CD7F32", 
                            "display": "flex", 
                            "alignItems": "flex-end",
                            "justifyContent": "center",
                            "padding": "5px"
                        }),
                        html.Div([
                            html.Div(top_players.index[2] if len(top_players) > 2 else "", 
                                    className="font-weight-bold text-center"),
                            html.Div(f"{top_players.iloc[2] if len(top_players) > 2 else 0} acciones", 
                                    className="small text-center")
                        ])
                    ], width=4, className="text-center")
                ], className="mt-2 mb-2"),
                
                # Mostrar otros jugadores
                html.Div([
                    html.Div("Otros jugadores:", className="font-weight-bold mt-3"),
                    html.Div([
                        html.Div(f"{player}: {count} acciones", className="small")
                        for player, count in filtered_df['Player'].value_counts().iloc[3:8].items()
                    ]) if len(filtered_df['Player'].value_counts()) > 3 else None
                ])
            ])
        else:
            jugadores_destacados = html.P("No hay datos de jugadores disponibles", className="text-muted")
    
    # Crear el componente de detalle
    detail = html.Div([
        # Encabezado con información general
        dbc.Card([
            dbc.CardHeader([
                html.H5("Resumen de Datos Filtrados", className="mb-0")
            ]),
            dbc.CardBody([
                dbc.Row([
                    # COLUMNA 1: Resumen general
                    dbc.Col([
                        html.H5("Resumen General", className="mb-3"),
                        dbc.Row([
                            # Total registros
                            dbc.Col([
                                html.Div([
                                    html.I(className="fas fa-database fa-3x", style={"color": "#0047AB"}),
                                ], className="text-center"),
                                html.Div([
                                    html.Div(f"{len(filtered_df)}", className="text-center font-weight-bold", style={"fontSize": "24px"}),
                                    html.Div("Total registros", className="text-center small")
                                ])
                            ], width=6, className="mb-3"),
                            
                            # Jornada
                            dbc.Col([
                                html.Div([
                                    html.I(className="fas fa-calendar-alt fa-3x", style={"color": "#E60026"}),
                                ], className="text-center"),
                                html.Div([
                                    html.Div(f"{jornada if jornada else 'Todas'}", className="text-center font-weight-bold", style={"fontSize": "24px"}),
                                    html.Div("Jornada", className="text-center small")
                                ])
                            ], width=6, className="mb-3"),
                        ]),
                        
                        # Rival (solo si está disponible)
                        html.Div([
                            html.Div([
                                html.I(className="fas fa-shield-alt mr-2", style={"color": "#0047AB"}),
                                html.Span("Rival:", className="font-weight-bold ml-2"),
                                html.Span(rival_info, className="ml-2")
                            ], className="d-flex align-items-center mb-3")
                        ]) if rival_info else None,

                        # Resultado (solo si está disponible)
                        html.Div([
                            html.Div([
                                html.I(className="fas fa-futbol mr-2", style={"color": "#E60026"}),
                                html.Span("Resultado:", className="font-weight-bold ml-2"),
                                html.Span(f"Alondras {resultado_info} {rival_info}", className="ml-2")
                            ], className="d-flex align-items-center mb-3")
                        ]) if resultado_info else None
                    ], width=4),
                    
                    # COLUMNA 2: Distribución por categoría
                    dbc.Col([
                        html.H5("Distribución por Categoría", className="mb-3"),
                        dbc.Card([
                            dbc.CardBody(crear_distribucion_categorias(filtered_df))
                        ])
                    ], width=4),
                    
                    # COLUMNA 3: Jugadores destacados (formato podio)
                    dbc.Col([
                        html.H5("Jugadores Destacados", className="mb-3"),
                        dbc.Card([
                            dbc.CardBody(jugadores_destacados)
                        ])
                    ], width=4),
                ], className="mb-4"),
                                
                # Vista previa de datos
                dbc.Row([
                    dbc.Col([
                        html.H5([
                            "Vista previa de datos ",
                            html.Span(f"(mostrando 5 de {len(filtered_df)})", className="small text-muted")
                        ], className="mb-3"),
                        
                        dbc.Table.from_dataframe(
                            filtered_df[['Descripción', 'code', 'group', 'Player', 'Periodo']].head(5) 
                            if len(filtered_df) > 0 else pd.DataFrame(),
                            striped=True,
                            bordered=True,
                            hover=True,
                            responsive=True,
                            size="sm"
                        ),
                        
                        dbc.Collapse(
                            dbc.Table.from_dataframe(
                                filtered_df[['Descripción', 'code', 'group', 'Player', 'Periodo']].iloc[5:] 
                                if len(filtered_df) > 5 else pd.DataFrame(),
                                striped=True,
                                bordered=True,
                                hover=True,
                                responsive=True,
                                size="sm"
                            ),
                            id="collapsed-data",
                            is_open=False
                        ),
                        
                        html.Div([
                            dbc.Button(
                                [
                                    html.I(className="fas fa-chevron-down mr-2"),
                                    "Ver todos los datos"
                                ], 
                                id="ver-mas-datos", 
                                color="primary", 
                                size="sm", 
                                className="mt-2"
                            )
                        ], className="text-right")
                    ], width=12)
                ])
            ])
        ], className="mb-4")
    ])

    return detail

# Esta función no estaba en tu código original pero es útil para normalizar coordenadas
def normalize_coordinates(df):
    """
    Normaliza las coordenadas para asegurar que están en el rango 0-100
    """
    if 'startX' in df.columns and 'startY' in df.columns and 'endX' in df.columns and 'endY' in df.columns:
        # Detectar el rango actual (valores máximos)
        max_x = max(df['startX'].max(), df['endX'].max())
        max_y = max(df['startY'].max(), df['endY'].max())
        
        # Si las coordenadas parecen ser diferentes de 0-100, normalizar
        if max_x > 100 or max_y > 100:
            # Dimensiones del campo (270x170 en este caso)
            df['startX'] = (df['startX'] / 270) * 100
            df['endX'] = (df['endX'] / 270) * 100
            
            # Invertir el eje Y para que 0 esté abajo
            df['startY'] = 100 - ((df['startY'] / 170) * 100)
            df['endY'] = 100 - ((df['endY'] / 170) * 100)
            
            # Asegurar que estén en rango 0-100
            df['startX'] = df['startX'].clip(0, 100)
            df['startY'] = df['startY'].clip(0, 100)
            df['endX'] = df['endX'].clip(0, 100)
            df['endY'] = df['endY'].clip(0, 100)
    
    return df