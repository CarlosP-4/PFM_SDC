import dash
from dash import html, callback, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd

# Importar funciones de utilidad
from utils.data_processing import load_data

def register_home_callbacks(app):
    """
    Registra todos los callbacks relacionados con la página de inicio
    """
    
    # Callback para actualizar el resumen del equipo en la página Home
    @app.callback(
        Output('team-summary', 'children'),
        [Input('session-data', 'data')]
    )
    def update_team_summary(session_data):
        if not session_data or not session_data.get('authenticated'):
            return dash.no_update
        
        try:
            df = load_data()
            
            # Para obtener información por partido, necesitamos agrupar por Descripción
            # y contar cada partido solo una vez
            partidos_df = df.drop_duplicates(subset=['Descripción'])
            
            # Obtener jornadas únicas
            jornadas_unicas = partidos_df['jornada'].unique() if 'jornada' in partidos_df.columns else []
            num_jornadas = len([j for j in jornadas_unicas if pd.notna(j)])
            
            # Contar partidos como local y visitante
            partidos_local = partidos_df['es_local'].sum() if 'es_local' in partidos_df.columns else 0
            partidos_visitante = partidos_df['es_visitante'].sum() if 'es_visitante' in partidos_df.columns else 0
            total_partidos = partidos_local + partidos_visitante
            
            # Sumar goles a favor y en contra
            goles_favor = partidos_df['goles_favor'].sum() if 'goles_favor' in partidos_df.columns else 0
            goles_contra = partidos_df['goles_contra'].sum() if 'goles_contra' in partidos_df.columns else 0
            diferencia_goles = goles_favor - goles_contra
            
            # Contar victorias y derrotas
            if 'resultado' in partidos_df.columns:
                victorias = (partidos_df['resultado'] == 'Victoria').sum()
                derrotas = (partidos_df['resultado'] == 'Derrota').sum()
            else:
                victorias = derrotas = 0
            
            # Calcular puntos
            puntos = victorias * 3
            puntos_posibles = total_partidos * 3 if total_partidos > 0 else 0
            eficiencia = round((puntos / puntos_posibles * 100) if puntos_posibles > 0 else 0, 1)
            
            # Crear tarjetas más atractivas con iconos y mejor estilo (con número debajo del texto)
            return html.Div([
                # Encabezado general con estadísticas principales
                html.Div([
                    # Cabecera con puntos
                    html.Div([
                        dbc.Card([
                            dbc.CardBody([
                                html.Div([
                                    html.I(className="fas fa-trophy", style={"fontSize": "24px", "color": "#FFD700", "marginRight": "10px"}),
                                    html.Span("Puntos:", style={"fontWeight": "bold"}),
                                ], style={"textAlign": "center"}),
                                html.Div([
                                    html.Span(f"{puntos}/{puntos_posibles} ({eficiencia}%)", style={"fontSize": "18px"}),
                                ], style={"textAlign": "center", "marginTop": "5px"})
                            ])
                        ], className="border-0")
                    ], className="col-6"),
                    
                    # Cabecera con goles
                    html.Div([
                        dbc.Card([
                            dbc.CardBody([
                                html.Div([
                                    html.I(className="fas fa-futbol", style={"fontSize": "24px", "color": "#28a745", "marginRight": "10px"}),
                                    html.Span("Goles:", style={"fontWeight": "bold"}),
                                ], style={"textAlign": "center"}),
                                html.Div([
                                    html.Span(f"{goles_favor} a favor / {goles_contra} en contra", style={"fontSize": "18px"}),
                                ], style={"textAlign": "center", "marginTop": "5px"})
                            ])
                        ], className="border-0")
                    ], className="col-6"),
                ], className="row mb-3"),
                
                # Tarjetas con estadísticas agrupadas en filas
                html.Div([
                    # Primera fila - 3 tarjetas
                    html.Div([
                        # Tarjeta de jornadas
                        html.Div([
                            dbc.Card([
                                dbc.CardBody([
                                    html.Div([
                                        html.I(className="fas fa-calendar-alt", 
                                               style={"fontSize": "36px", "color": "#007bff", "display": "block", 
                                                      "textAlign": "center", "marginBottom": "10px"}),
                                        html.H3(f"{num_jornadas}", 
                                                style={"fontWeight": "bold", "textAlign": "center", "margin": "0"}),
                                        html.P("Jornadas analizadas", 
                                               style={"textAlign": "center", "color": "#6c757d", "marginTop": "5px"})
                                    ])
                                ])
                            ], className="shadow-sm h-100")
                        ], className="col-4 mb-3"),
                        
                        # Tarjeta de partidos como local/visitante
                        html.Div([
                            dbc.Card([
                                dbc.CardBody([
                                    html.Div([
                                        html.I(className="fas fa-home", 
                                               style={"fontSize": "36px", "color": "#6f42c1", "display": "block", 
                                                      "textAlign": "center", "marginBottom": "10px"}),
                                        html.H3(f"{partidos_local} / {partidos_visitante}", 
                                                style={"fontWeight": "bold", "textAlign": "center", "margin": "0"}),
                                        html.P("Local / Visitante", 
                                               style={"textAlign": "center", "color": "#6c757d", "marginTop": "5px"})
                                    ])
                                ])
                            ], className="shadow-sm h-100")
                        ], className="col-4 mb-3"),
                        
                        # Tarjeta de diferencia de goles
                        html.Div([
                            dbc.Card([
                                dbc.CardBody([
                                    html.Div([
                                        html.I(className="fas fa-balance-scale", 
                                               style={"fontSize": "36px", "color": "#fd7e14", "display": "block", 
                                                      "textAlign": "center", "marginBottom": "10px"}),
                                        html.H3(f"{diferencia_goles:+d}", 
                                                style={"fontWeight": "bold", "textAlign": "center", "margin": "0",
                                                       "color": "#28a745" if diferencia_goles > 0 else 
                                                                "#dc3545" if diferencia_goles < 0 else "#6c757d"}),
                                        html.P("Diferencia de goles", 
                                               style={"textAlign": "center", "color": "#6c757d", "marginTop": "5px"})
                                    ])
                                ])
                            ], className="shadow-sm h-100")
                        ], className="col-4 mb-3"),
                    ], className="row"),
                    
                    # Segunda fila - 2 tarjetas
                    html.Div([
                        # Tarjeta de victorias
                        html.Div([
                            dbc.Card([
                                dbc.CardBody([
                                    html.Div([
                                        html.I(className="fas fa-check-circle", 
                                               style={"fontSize": "36px", "color": "#28a745", "display": "block", 
                                                      "textAlign": "center", "marginBottom": "10px"}),
                                        html.H3(f"{victorias}", 
                                                style={"fontWeight": "bold", "textAlign": "center", "margin": "0"}),
                                        html.P("Victorias", 
                                               style={"textAlign": "center", "color": "#6c757d", "marginTop": "5px"})
                                    ])
                                ])
                            ], className="shadow-sm h-100", style={"borderLeft": "5px solid #28a745"})
                        ], className="col-6 mb-3"),
                        
                        # Tarjeta de derrotas
                        html.Div([
                            dbc.Card([
                                dbc.CardBody([
                                    html.Div([
                                        html.I(className="fas fa-times-circle", 
                                               style={"fontSize": "36px", "color": "#dc3545", "display": "block", 
                                                      "textAlign": "center", "marginBottom": "10px"}),
                                        html.H3(f"{derrotas}", 
                                                style={"fontWeight": "bold", "textAlign": "center", "margin": "0"}),
                                        html.P("Derrotas", 
                                               style={"textAlign": "center", "color": "#6c757d", "marginTop": "5px"})
                                    ])
                                ])
                            ], className="shadow-sm h-100", style={"borderLeft": "5px solid #dc3545"})
                        ], className="col-6 mb-3"),
                    ], className="row"),
                    
                    # Tercera fila - Gráfico de eficiencia de puntos
                    html.Div([
                        html.Div([
                            dbc.Card([
                                dbc.CardHeader("Eficiencia de puntos", className="text-center"),
                                dbc.CardBody([
                                    dbc.Progress(
                                        value=eficiencia, 
                                        color="success" if eficiencia >= 70 else "warning" if eficiencia >= 40 else "danger",
                                        striped=True,
                                        animated=True,
                                        className="mb-2",
                                        style={"height": "20px"}  # Barra más alta para mejor visibilidad
                                    ),
                                    html.P(f"{eficiencia}% de los puntos posibles", 
                                           className="text-center", 
                                           style={"marginTop": "10px", "marginBottom": "0"})
                                ])
                            ], className="shadow-sm")
                        ], className="col-12 mb-3"),
                    ], className="row"),
                ]),
            ])
            
        except Exception as e:
            print(f"Error al generar resumen del equipo: {e}")
            import traceback
            traceback.print_exc()
            return html.P(f"Error al generar el resumen: {str(e)}")

    # Callback para actualizar la tabla de resumen de jornadas
    @app.callback(
        Output('match-summary-table', 'children'),
        [Input('session-data', 'data')]
    )
    def update_match_summary(session_data):
        if not session_data or not session_data.get('authenticated'):
            return dash.no_update
        
        try:
            df = load_data()
            
            # Crear un dataframe con información única por jornada
            if 'Descripción' in df.columns:
                # Obtener descripciones únicas (partidos únicos)
                unique_matches = df.drop_duplicates(subset=['Descripción'])
                
                # Crear dataframe de resumen
                match_summary = pd.DataFrame({
                    'Jornada': unique_matches['jornada'],
                    'Local': unique_matches['equipo_local'],
                    'Visitante': unique_matches['equipo_visitante'],
                    'Resultado': unique_matches['goles_local'].astype(str) + '-' + unique_matches['goles_visitante'].astype(str),
                    'Puntos': unique_matches['puntos'],
                    'Condición': unique_matches.apply(lambda x: 'Local' if x['es_local'] else 'Visitante', axis=1)
                }).sort_values('Jornada')
                
                # Crear tabla HTML personalizada en lugar de usar style_data_conditional
                styled_rows = []
                for _, row in match_summary.iterrows():
                    # Determinar el estilo de la fila según el resultado
                    if row['Puntos'] == 3:
                        row_style = {'backgroundColor': 'rgba(40, 167, 69, 0.2)'}  # Verde claro para victoria
                    else:
                        row_style = {'backgroundColor': 'rgba(220, 53, 69, 0.2)'}  # Rojo claro para derrota
                    
                    styled_rows.append(html.Tr([
                        html.Td(row['Jornada']),
                        html.Td(row['Local']),
                        html.Td(row['Visitante']),
                        html.Td(row['Resultado']),
                        html.Td(row['Puntos']),
                        html.Td(row['Condición'])
                    ], style=row_style))
                
                styled_table = html.Table([
                    html.Thead(html.Tr([
                        html.Th("Jornada", style={"backgroundColor": "#f8f9fa", "color": "#343a40"}),
                        html.Th("Local", style={"backgroundColor": "#f8f9fa", "color": "#343a40"}),
                        html.Th("Visitante", style={"backgroundColor": "#f8f9fa", "color": "#343a40"}),
                        html.Th("Resultado", style={"backgroundColor": "#f8f9fa", "color": "#343a40"}),
                        html.Th("Puntos", style={"backgroundColor": "#f8f9fa", "color": "#343a40"}),
                        html.Th("Condición", style={"backgroundColor": "#f8f9fa", "color": "#343a40"})
                    ], style={"borderBottom": "2px solid #007bff"})),
                    html.Tbody(styled_rows)
                ], 
                className="table table-bordered table-hover table-striped table-responsive w-100",
                style={
                    'fontSize': '0.9rem',
                    'width': '100%',
                    'maxWidth': '100%',
                    'boxShadow': '0 2px 3px rgba(0,0,0,0.1)'
                })
                
                return styled_table
            else:
                return html.P("No hay datos de jornadas disponibles")
        
        except Exception as e:
            print(f"Error al generar tabla de jornadas: {e}")
            import traceback
            traceback.print_exc()
            return html.P(f"Error al generar la tabla: {str(e)}")