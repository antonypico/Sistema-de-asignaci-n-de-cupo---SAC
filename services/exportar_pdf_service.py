"""
Servicio para exportar resultados a PDF
"""
import json
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
from datetime import datetime


class ExportarPDFService:
    
    @staticmethod
    def exportar_pdf(resultados):
        """
        Exporta resultados a PDF en formato tabla
        """
        # Crear buffer en memoria
        buffer = BytesIO()
        
        # Crear documento PDF
        doc = SimpleDocTemplate(
            buffer,
            pagesize=landscape(A4),
            rightMargin=0.5 * inch,
            leftMargin=0.5 * inch,
            topMargin=0.75 * inch,
            bottomMargin=0.5 * inch
        )
        
        # Contenedor de elementos
        elements = []
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#2d3748'),
            spaceAfter=12,
            alignment=TA_CENTER
        )
        
        # Título
        titulo = Paragraph("RESULTADOS DE ASIGNACIÓN DE CUPOS", title_style)
        elements.append(titulo)
        
        # Fecha y cantidad
        fecha_str = datetime.now().strftime("%d/%m/%Y %H:%M")
        info_style = ParagraphStyle(
            'Info',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#718096'),
            alignment=TA_CENTER,
            spaceAfter=12
        )
        info = Paragraph(f"Generado: {fecha_str} | Total: {len(resultados)} postulantes", info_style)
        elements.append(info)
        elements.append(Spacer(1, 0.2 * inch))
        
        # Preparar datos para la tabla
        datos_tabla = [
            [
                'ID Postulante',
                'Estudiante',
                'Segmento',
                'Carrera Asignada',
                'Jornada',
                'Modalidad',
                'Estado',
                'Observaciones'
            ]
        ]
        
        # Agregar filas de datos
        for resultado in resultados:
            fila = [
                str(resultado.get('id_estudiante', '')),
                f"{resultado.get('nombres', '')} {resultado.get('apellidos', '')}",
                str(resultado.get('segmento', 'N/A')),
                str(resultado.get('carrera', 'N/A')),
                str(resultado.get('jornada', '-')),
                str(resultado.get('modalidad', '-')),
                str(resultado.get('estado_asignacion', 'N/A')),
                str(resultado.get('razon_no_asignacion', 'Asignación exitosa')[:50])  # Limitar a 50 caracteres
            ]
            datos_tabla.append(fila)
        
        # Crear tabla
        tabla = Table(datos_tabla, repeatRows=1)
        
        # Estilos de tabla
        estilo_tabla = TableStyle([
            # Encabezado
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            # Contenido
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),  # ID Postulante centrado
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            
            # Bordes
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            
            # Filas alternadas
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7fafc')]),
        ])
        
        tabla.setStyle(estilo_tabla)
        elements.append(tabla)
        
        # Generar PDF
        doc.build(elements)
        
        # Obtener bytes del PDF
        buffer.seek(0)
        return buffer
