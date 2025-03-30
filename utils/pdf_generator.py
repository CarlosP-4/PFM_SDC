from fpdf import FPDF
import pandas as pd

def create_pdf(filtered_data):
    """
    Crea un PDF simple con la información del dataframe filtrado
    """
    # Verificaciones iniciales
    if filtered_data is None or len(filtered_data) == 0:
        print("Advertencia: Dataframe vacío o None")
        return None
    
    # Crear PDF
    pdf = FPDF()
    pdf.add_page()
    
    # Configurar fuente
    pdf.set_font("Arial", size=12)
    
    # Título
    pdf.cell(200, 10, txt="Informe Detallado Alondras F.C.", ln=True, align='C')
    pdf.ln(10)
    
    # Información general
    pdf.cell(200, 10, txt=f"Total de registros: {len(filtered_data)}", ln=True)
    pdf.ln(10)
    
    # Columnas a mostrar
    columnas = ['Descripción', 'Periodo', 'code', 'group', 'Player']
    
    # Encabezados
    pdf.set_font("Arial", 'B', 10)
    for col in columnas:
        pdf.cell(40, 10, col, border=1)
    pdf.ln()
    
    # Datos
    pdf.set_font("Arial", size=8)
    for _, row in filtered_data.head(30).iterrows():
        for col in columnas:
            valor = str(row[col]) if col in row.index and pd.notna(row[col]) else '-'
            # Truncar valores largos
            valor = (valor[:20] + '...') if len(valor) > 20 else valor
            pdf.cell(40, 7, valor, border=1)
        pdf.ln()
    
    # Generar PDF en memoria
    from io import BytesIO
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)
    
    return pdf_buffer.getvalue()