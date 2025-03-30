import pandas as pd
from dash import html, Input, Output, State, callback, dcc
import dash
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
from datetime import datetime
from io import StringIO

# Importar funciones de utilidad
from utils.data_processing import load_data, create_pdf
from utils.visualization import (
    create_improved_campograma, 
    evaluate_all_actions,
    assign_zones_by_pass_direction,
    crear_efectividad_mejorada,
    crear_distribucion_categorias,
    crear_detalle_filtrado,
    crear_donut_efectividad
)

def register_stats_callbacks(app):
    @app.callback(
        [Output('jornada-dropdown', 'options'),
         Output('category-dropdown', 'options'),
         Output('group-dropdown', 'options')],
        [Input('page-content', 'children')],
        [State('session-data', 'data')]
    )
    def load_initial_data(content, session_data):
        """
        Carga los datos iniciales para los dropdowns
        """
        if not session_data or not session_data.get('authenticated'):
            return [], [], []
        
        try:
            # Cargar datos
            df = load_data()
            
            # Extraer jornadas únicas de la columna Descripción
            jornadas = []
            if 'Descripción' in df.columns:
                # Extraer patrones como "J18" de la columna Descripción
                jornada_pattern = df['Descripción'].str.extract(r'(J\d+)', expand=False)
                jornada_unique = jornada_pattern.dropna().unique()
                jornadas = [{'label': j, 'value': j} for j in sorted(jornada_unique)]
            
            # Opciones para categorías y grupos
            category_options = []
            group_options = []
            
            if 'code' in df.columns:
                category_options = [
                    {'label': cat, 'value': cat} 
                    for cat in sorted(df['code'].dropna().unique())
                ]
            
            if 'group' in df.columns:
                group_options = [
                    {'label': group, 'value': group} 
                    for group in sorted(df['group'].dropna().unique())
                ]
            
            return jornadas, category_options, group_options
        
        except Exception as e:
            print(f"Error al cargar datos iniciales: {e}")
            return [], [], []

    @app.callback(
        [Output('filtered-data', 'data'),
         Output('filtered-data-detail', 'children'),
         Output('campograma-plot', 'figure'),
         Output('group-distribution', 'figure'),
         Output('zona-vertical-stats', 'children'),
         Output('pasillo-stats', 'children')],
        [Input('apply-filters', 'n_clicks')],
        [State('jornada-dropdown', 'value'),
         State('period-check', 'value'),
         State('category-dropdown', 'value'),
         State('group-dropdown', 'value')]
    )
    def update_stats(n_clicks, jornada, periods, category, group):
        """
        Actualiza las visualizaciones según los filtros seleccionados
        """
        if n_clicks is None:
            # Valores predeterminados
            empty_fig = go.Figure()
            empty_fig.update_layout(title="Aplica filtros para ver datos")
            return None, html.P("Aplica filtros para ver los datos"), empty_fig, empty_fig, "", ""
        
        try:
            # Cargar datos
            df = load_data()
            print(f"Datos cargados exitosamente: {len(df)} filas")
            
            # Crear una copia para aplicar filtros
            filtered_df = df.copy()
            print(f"Datos copiados: {len(filtered_df)} filas")
            
            # Filtro de jornada desde la columna Descripción (mejorado)
            if jornada and 'Descripción' in filtered_df.columns:
                try:
                    print(f"Aplicando filtro de jornada: {jornada}")
                    # Extraer exactamente el patrón de jornada seleccionado (J18, J21, etc.)
                    filtered_df = filtered_df[filtered_df['Descripción'].str.contains(f"{jornada}_", regex=False, na=False)]
                    print(f"Después de filtro de jornada: {len(filtered_df)} filas")
                except Exception as e:
                    print(f"Error en filtro de jornada: {e}")
            
            # Filtro de periodo
            if periods and 'Periodo' in filtered_df.columns:
                try:
                    print(f"Aplicando filtro de periodo: {periods}")
                    filtered_df = filtered_df[filtered_df['Periodo'].isin(periods)]
                    print(f"Después de filtro de periodo: {len(filtered_df)} filas")
                except Exception as e:
                    print(f"Error en filtro de periodo: {e}")
            
            # Filtro de categoría
            if category and 'code' in filtered_df.columns:
                try:
                    print(f"Aplicando filtro de categoría: {category}")
                    filtered_df = filtered_df[filtered_df['code'] == category]
                    print(f"Después de filtro de categoría: {len(filtered_df)} filas")
                except Exception as e:
                    print(f"Error en filtro de categoría: {e}")
            
            # Filtro de grupo
            if group and 'group' in filtered_df.columns:
                try:
                    print(f"Aplicando filtro de grupo: {group}")
                    filtered_df = filtered_df[filtered_df['group'] == group]
                    print(f"Después de filtro de grupo: {len(filtered_df)} filas")
                except Exception as e:
                    print(f"Error en filtro de grupo: {e}")
            
            # Asegurar que haya datos para visualizar
            if filtered_df.empty:
                print("ADVERTENCIA: Conjunto de datos filtrado está vacío")
                empty_fig = go.Figure()
                empty_fig.update_layout(
                    title="No hay datos que cumplan con los filtros seleccionados",
                    xaxis=dict(visible=False),
                    yaxis=dict(visible=False)
                )
                return None, html.P("No hay datos que cumplan con los filtros seleccionados"), empty_fig, empty_fig, "", ""
            
            # 1. Normalizar coordenadas
            filtered_df_normalized = filtered_df.copy()
            if 'startX' in filtered_df.columns and 'startY' in filtered_df.columns and 'endX' in filtered_df.columns and 'endY' in filtered_df.columns:
                # Normalización usando las dimensiones proporcionadas (270x170)
                filtered_df_normalized['startX'] = (filtered_df['startX'] / 270) * 100
                filtered_df_normalized['endX'] = (filtered_df['endX'] / 270) * 100
                
                # Invertir el eje Y para que 0 esté abajo
                filtered_df_normalized['startY'] = 100 - ((filtered_df['startY'] / 170) * 100)
                filtered_df_normalized['endY'] = 100 - ((filtered_df['endY'] / 170) * 100)
                
                # Asegurar que estén en rango 0-100
                filtered_df_normalized['startX'] = filtered_df_normalized['startX'].clip(0, 100)
                filtered_df_normalized['startY'] = filtered_df_normalized['startY'].clip(0, 100)
                filtered_df_normalized['endX'] = filtered_df_normalized['endX'].clip(0, 100)
                filtered_df_normalized['endY'] = filtered_df_normalized['endY'].clip(0, 100)

            # 2. Manejar valores nulos
            if 'code' in filtered_df_normalized.columns:
                problematic_categories = ["Llegadas extremo area", "Llegadas extremos area", "Trans. Def", "Trans. Of"]
                for category in problematic_categories:
                    category_mask = filtered_df_normalized['code'] == category
                    if category_mask.any():
                        # Verificar si hay valores nulos en startX
                        null_startx = filtered_df_normalized.loc[category_mask, 'startX'].isna()
                        if null_startx.any():
                            print(f"Reparando {null_startx.sum()} valores nulos en startX para '{category}'")
                            # Usar la media de los valores no nulos para esta categoría, o 50 si todos son nulos
                            mean_startx = filtered_df_normalized.loc[category_mask & ~filtered_df_normalized['startX'].isna(), 'startX'].mean()
                            filtered_df_normalized.loc[category_mask & null_startx, 'startX'] = mean_startx if not pd.isna(mean_startx) else 50

            # 3. Añadir identificación de pasillos (no cambia con el periodo)
            filtered_df_normalized['pasillo'] = filtered_df_normalized.apply(
                lambda row: "Pasillo Lateral" if row["startY"] < 25 or row["startY"] >= 75 else "Pasillo Central", 
                axis=1
            )

            # 4. Asignar zonas verticales con la función especializada
            filtered_df_normalized = assign_zones_by_pass_direction(filtered_df_normalized)

            # VISUALIZACIÓN 1: Campograma interactivo mejorado
            campo_fig = create_improved_campograma(filtered_df_normalized, jornada, periods)
            
            # VISUALIZACIÓN 2: Distribución por categorías
            if 'group' in filtered_df.columns:
                # Eliminar cualquier subgrupo si hay una separación por coma
                filtered_df['group_main'] = filtered_df['group'].astype(str).str.split(',').str[0]
                
                # Contar por grupo principal
                group_counts = filtered_df['group_main'].value_counts().reset_index()
                group_counts.columns = ['Tipo', 'Cantidad']
                
                # Categorizar los grupos para ordenarlos y colorearlos
                def categorize_group(group):
                    if 'Largo' in group:
                        return "1-Pases en Largo"
                    elif 'DFC' in group:
                        return "2-DFC"
                    elif 'MC' in group:
                        return "3-MC"
                    elif 'Centros' in group:
                        return "4-Centros en Llegada"
                    elif 'Robo' in group or 'No Robo' in group:
                        return "5-Transiciones Defensivas"
                    elif 'Perdida' in group or 'Sacado' in group:
                        return "6-Transiciones Ofensivas"
                    elif 'Generar' in group or 'Recibir' in group:
                        return "7-Llegadas Extremo"
                    else:
                        return "8-Otros"
                
                group_counts['Categoría'] = group_counts['Tipo'].apply(categorize_group)
                group_counts = group_counts.sort_values(['Categoría', 'Cantidad'], ascending=[True, False])
                
                # Mapa de colores exactos de la visualización 1 (simplificado)
                color_dict = {
                    "Largo (C) ocasión de gol": "#000080",
                    "Largo (I) conlleva perdida": "#87CEEB",
                    "DFC campo rival (C)": "#4B0082",
                    "Centros en llegada (C)": "#FF4500",
                    "Generar espacio (C)": "#06402B",
                    "Robo": "#FF00FF",
                    "No Robo": "#00FFFF"
                }
                
                # Crear gráfico de barras con colores individuales
                group_fig = px.bar(
                    group_counts,
                    x='Tipo',  # Usar los nombres originales
                    y='Cantidad',
                    color='Tipo',
                    title='Distribución por Tipo de Acción',
                    text='Cantidad',
                    color_discrete_map=color_dict
                )
                
                # Personalizar el diseño para mejor visualización
                group_fig.update_layout(
                    xaxis_title='',
                    yaxis_title='Cantidad',
                    plot_bgcolor='white',  # Fondo del área de trazado blanco
                    paper_bgcolor='white',  # Fondo del papel blanco
                    xaxis={
                        'categoryorder':'array', 
                        'categoryarray': group_counts['Tipo'].tolist(),
                        'tickangle': 45
                    },
                    height=600,
                    font=dict(family="Arial, sans-serif", size=10),
                    showlegend=False,
                    margin=dict(l=40, r=40, t=60, b=180)
                )
                
                # Ajustar etiquetas para mejor visualización
                group_fig.update_xaxes(
                    tickfont=dict(size=9, family="Arial, sans-serif", color="black"),
                    tickmode='array',
                    tickvals=group_counts['Tipo'].tolist()
                )
                
                # Ajustar el texto sobre las barras - más grande y en negrita
                group_fig.update_traces(
                    textposition='outside',
                    textfont=dict(
                        size=14,
                        family="Arial, sans-serif",
                        color="black"
                    ),
                    hovertemplate='<b>%{text}</b> acciones<br>%{x}'
                )
            else:
                group_fig = go.Figure()
                group_fig.update_layout(
                    title="No hay datos de tipos disponibles",
                    paper_bgcolor='rgba(240, 240, 240, 0.8)',
                    plot_bgcolor='rgba(240, 240, 240, 0.8)',
                    height=600
                )

            # VISUALIZACIÓN 3: Estadísticas por zona vertical
            if 'zona_vertical' in filtered_df_normalized.columns:
                # Calcular métricas por zona
                zona_metrics = {}
                for zona in ["Zona Defensiva", "Zona Pre-Defensiva", "Zona Pre-Ofensiva", "Zona Ofensiva"]:
                    # Importante: Filtramos por zona_vertical, que ya considera el periodo
                    zona_df = filtered_df_normalized[filtered_df_normalized['zona_vertical'] == zona]
                    
                    total = len(zona_df)
                    percentage = (total / len(filtered_df_normalized) * 100) if len(filtered_df_normalized) > 0 else 0
                    
                    # Usar la función de evaluación para todas las categorías
                    if 'group' in zona_df.columns and 'code' in zona_df.columns and total > 0:
                        evaluation = evaluate_all_actions(zona_df)
                        correctos = evaluation['correctos']
                        incorrectos = evaluation['incorrectos']
                        no_evaluados = evaluation.get('no_evaluados', 0)
                        efectividad = evaluation['efectividad']
                        total_evaluados = correctos + incorrectos
                    else:
                        correctos = 0
                        incorrectos = 0
                        no_evaluados = total
                        efectividad = 0
                        total_evaluados = 0
                    
                    zona_metrics[zona] = {
                        'total': total,
                        'percentage': percentage,
                        'efectividad': efectividad,
                        'correctos': correctos,
                        'incorrectos': incorrectos,
                        'no_evaluados': no_evaluados,
                        'total_evaluados': total_evaluados
                    }
                
                # Crear tarjetas mejoradas para cada zona
                zona_cards = []
                zonas_orden = ["Zona Defensiva", "Zona Pre-Defensiva", "Zona Pre-Ofensiva", "Zona Ofensiva"]
                
                for zona in zonas_orden:
                    metrics = zona_metrics[zona]
                    
                    # Estilo según efectividad - solo si hay acciones evaluadas
                    if metrics['total_evaluados'] > 0:
                        if metrics['efectividad'] >= 80:
                            efectividad_color = "success"
                        elif metrics['efectividad'] >= 60:
                            efectividad_color = "warning"
                        else:
                            efectividad_color = "danger"
                    else:
                        efectividad_color = "secondary"
                    
                    zona_cards.append(
                        dbc.Card([
                            dbc.CardHeader(zona, className="text-center"),
                            dbc.CardBody([
                                html.H4(f"{metrics['total']}", className="text-center"),
                                html.P(f"{metrics['percentage']:.1f}% del total", className="text-center"),
                                html.Hr(className="my-2"),
                                # Mostrar desglose de acciones
                                html.Div([
                                    html.P([
                                        html.I(className="fas fa-check mr-2", style={"color": "#28a745"}),
                                        f"Correctas: {metrics['correctos']}"
                                    ], className="mb-1"),
                                    html.P([
                                        html.I(className="fas fa-times text-danger mr-2"),
                                        f"Incorrectas: {metrics['incorrectos']}"
                                    ], className="mb-1"),
                                    html.P([
                                        html.I(className="fas fa-question-circle text-secondary mr-2"),
                                        f"No evaluadas: {metrics['no_evaluados']}"
                                    ], className="mb-1") if metrics.get('no_evaluados', 0) > 0 else None
                                ], className="text-center mb-2"),
                                # Mostrar efectividad (versión original con span coloreado)
                                html.Div([
                                    html.Span("Efectividad: ", className="mr-2"),
                                    html.Span(
                                        f"{metrics['efectividad']:.1f}%", 
                                        className="ml-1 px-2 py-1 rounded",
                                        style={
                                            "backgroundColor": 
                                                "#28a745" if metrics['efectividad'] >= 80 else 
                                                "#ffc107" if metrics['efectividad'] >= 60 else 
                                                "#dc3545",
                                            "color": "white",
                                            "fontWeight": "bold",
                                            "fontSize": "85%"
                                        }
                                    )
                                ], className="text-center") if metrics['total_evaluados'] > 0 else 
                                html.P("Sin datos suficientes para calcular efectividad", 
                                    className="text-center text-muted small")
                            ])
                        ], className="mb-2", color="light")
                    )
                
                # Crear las tarjetas de zonas sin efectividad general
                zona_stats = html.Div(zona_cards)
            else:
                zona_stats = html.P("No hay datos de zonas verticales disponibles")

            # VISUALIZACIÓN 4: Estadísticas por pasillo
            if 'pasillo' in filtered_df_normalized.columns:
                # Calcular métricas por pasillo
                pasillo_metrics = {}
                for pasillo in ["Pasillo Lateral", "Pasillo Central"]:
                    pasillo_df = filtered_df_normalized[filtered_df_normalized['pasillo'] == pasillo]
                    
                    total = len(pasillo_df)
                    percentage = (total / len(filtered_df_normalized) * 100) if len(filtered_df_normalized) > 0 else 0
                    
                    # Usar la función de evaluación refinada
                    if 'group' in pasillo_df.columns and 'code' in pasillo_df.columns and total > 0:
                        evaluation = evaluate_all_actions(pasillo_df)
                        correctos = evaluation['correctos']
                        incorrectos = evaluation['incorrectos']
                        no_evaluados = evaluation['no_evaluados']
                        efectividad = evaluation['efectividad']
                        total_evaluados = evaluation['total_evaluados']
                    else:
                        correctos = 0
                        incorrectos = 0
                        no_evaluados = total
                        efectividad = 0
                        total_evaluados = 0
                    
                    pasillo_metrics[pasillo] = {
                        'total': total,
                        'percentage': percentage,
                        'efectividad': efectividad,
                        'correctos': correctos,
                        'incorrectos': incorrectos,
                        'no_evaluados': no_evaluados,
                        'total_evaluados': total_evaluados
                    }
                
                # Crear tarjetas mejoradas para cada pasillo
                pasillo_cards = []
                pasillos_orden = ["Pasillo Lateral", "Pasillo Central"]
                
                for pasillo in pasillos_orden:
                    metrics = pasillo_metrics[pasillo]
                    
                    # Estilo según efectividad - solo si hay acciones evaluadas
                    if metrics['total_evaluados'] > 0:
                        if metrics['efectividad'] >= 80: 
                            efectividad_color = "success"
                        elif metrics['efectividad'] >= 60:  
                            efectividad_color = "warning"
                        else:
                            efectividad_color = "danger"
                    else:
                        efectividad_color = "secondary"
                    
                    pasillo_cards.append(
                        dbc.Card([
                            dbc.CardHeader(pasillo, className="text-center"),
                            dbc.CardBody([
                                html.H4(f"{metrics['total']}", className="text-center"),
                                html.P(f"{metrics['percentage']:.1f}% del total", className="text-center"),
                                html.Hr(className="my-2"),
                                # Mostrar desglose de acciones
                                html.Div([
                                    html.P([
                                        html.I(className="fas fa-check mr-2", style={"color": "#28a745"}),
                                        f"Correctas: {metrics['correctos']}"
                                    ], className="mb-1"),
                                    html.P([
                                        html.I(className="fas fa-times text-danger mr-2"),
                                        f"Incorrectas: {metrics['incorrectos']}"
                                    ], className="mb-1"),
                                    html.P([
                                        html.I(className="fas fa-question-circle text-secondary mr-2"),
                                        f"No evaluadas: {metrics['no_evaluados']}"
                                    ], className="mb-1") if metrics['no_evaluados'] > 0 else None
                                ], className="text-center mb-2"),
                                # Mostrar efectividad solo si hay acciones evaluadas
                                html.Div([
                                    html.Span("Efectividad: ", className="mr-2"),
                                    html.Span(
                                        f"{metrics['efectividad']:.1f}%", 
                                        className="ml-1 px-2 py-1 rounded",
                                        style={
                                            "backgroundColor": 
                                                "#28a745" if metrics['efectividad'] >= 80 else 
                                                "#ffc107" if metrics['efectividad'] >= 60 else 
                                                "#dc3545",
                                            "color": "white",
                                            "fontWeight": "bold",
                                            "fontSize": "85%"
                                        }
                                    )
                                ], className="text-center") if metrics['total_evaluados'] > 0 else 
                                html.P("Sin datos suficientes para calcular efectividad", 
                                    className="text-center text-muted small")
                            ])
                        ], className="mb-2", color="light")
                    )
                
                # Calcular efectividad general
                general_evaluation = evaluate_all_actions(filtered_df_normalized)
                correctas_general = general_evaluation['correctos']
                incorrectas_general = general_evaluation['incorrectos']
                no_evaluadas_general = general_evaluation.get('no_evaluados', 0)
                total_evaluadas = correctas_general + incorrectas_general
                efectividad_general = (correctas_general / total_evaluadas * 100) if total_evaluadas > 0 else 0

                # Crear contenido del detalle de efectividad general con el nuevo diseño mejorado
                efectividad_general_content = crear_efectividad_mejorada(
                    correctas_general, 
                    incorrectas_general, 
                    no_evaluadas_general
                )
                
                # Añadir efectividad general después de los pasillos
                pasillo_stats = html.Div([
                    # Primero las tarjetas de pasillo
                    html.Div(pasillo_cards),
                    
                    # Luego la tarjeta de efectividad general
                    dbc.Card([
                        dbc.CardHeader("Efectividad General", className="text-center"),
                        dbc.CardBody(efectividad_general_content)
                    ], className="mt-3 shadow-sm")
                ])
            else:
                pasillo_stats = html.P("No hay datos de pasillos disponibles")
            
            # Crear detalle de datos filtrados con más información
            detail = crear_detalle_filtrado(filtered_df, jornada, periods, efectividad_general_content)
            
            # Convertir el dataframe a formato JSON para almacenarlo
            filtered_json = filtered_df.to_json(date_format='iso', orient='split')

            return filtered_json, detail, campo_fig, group_fig, zona_stats, pasillo_stats
            
        except Exception as e:
            print(f"Error al aplicar filtros: {e}")
            import traceback
            traceback.print_exc()
            
            # En caso de error, devolver figuras vacías
            empty_fig = go.Figure()
            empty_fig.update_layout(
                title=f"Error al procesar datos: {str(e)}",
                xaxis=dict(visible=False),
                yaxis=dict(visible=False)
            )
            
            error_detail = html.Div([
                html.H5("Error al procesar los datos", className="text-danger"),
                html.P(f"Detalles: {str(e)}")
            ])
            
            return None, error_detail, empty_fig, empty_fig, "", ""

    # Callback para manejar el botón "Ver más datos"
    @app.callback(
        [Output("collapsed-data", "is_open"),
         Output("ver-mas-datos", "children")],
        [Input("ver-mas-datos", "n_clicks")],
        [State("collapsed-data", "is_open")]
    )
    def toggle_more_data(n_clicks, is_open):
        if n_clicks:
            if is_open:
                return False, [html.I(className="fas fa-chevron-down mr-2"), "Ver todos los datos"]
            else:
                return True, [html.I(className="fas fa-chevron-up mr-2"), "Ver menos datos"]
        return False, [html.I(className="fas fa-chevron-down mr-2"), "Ver todos los datos"]

    @app.callback(
    Output('download-pdf', 'data'),
    [Input('export-pdf', 'n_clicks')],
    [State('filtered-data', 'data')],
    prevent_initial_call=True
    )
    def export_to_pdf(n_clicks, filtered_data):
        if n_clicks is None:
            return dash.no_update
        
        if filtered_data is None:
            return dash.no_update
        
        try:
            from io import StringIO
            
            # Convertir los datos JSON de vuelta a dataframe
            df_filtered = pd.read_json(StringIO(filtered_data), orient='split')
            
            # Crear el PDF
            pdf_bytes = create_pdf(df_filtered)
            
            # Devolver el PDF para descargar
            if pdf_bytes:
                return dcc.send_bytes(pdf_bytes, f"alondras_informe_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf")
            else:
                return dash.no_update
        
        except Exception as e:
            print("Error en exportación a PDF:", e)
            import traceback
            traceback.print_exc()
            return dash.no_update