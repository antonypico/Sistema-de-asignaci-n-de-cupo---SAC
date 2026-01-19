from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file, flash
from flask_cors import CORS
from datetime import datetime, date
import json
import os
import csv
import io
import pandas as pd
from werkzeug.utils import secure_filename
from collections import Counter

# Importar servicios
from services.periodo_service import PeriodoService, Periodo
from services.oferta_academica_service import OfertaAcademicaService
from services.postulante_service import PostulanteService
from services.asignacion_service import AsignacionService
from services.estadisticas_service import EstadisticasService
from services.exportar_resultados_service import ExportarResultadosService
from domain.oferta_academica import OfertaAcademica

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui_cambiar_en_produccion'
CORS(app)

# Configurar carpeta de uploads
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Servicios
periodo_service = PeriodoService()
oferta_service = OfertaAcademicaService()
postulante_service = PostulanteService()
asignacion_service = AsignacionService()
estadisticas_service = EstadisticasService()
exportar_service = ExportarResultadosService()

# ==================== AUTENTICACIÓN ====================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        clave = request.form.get('clave')
        
        # Credenciales fijas (suficientes para el proyecto)
        if usuario == 'admin' and clave == 'admin123':
            session['usuario'] = usuario
            return redirect(url_for('menu'))
        else:
            return render_template('login.html', error='Credenciales inválidas')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

def verificar_autenticacion(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== RUTAS PRINCIPALES ====================

@app.route('/')
def index():
    if 'usuario' in session:
        return redirect(url_for('menu'))
    return redirect(url_for('login'))

@app.route('/menu')
@verificar_autenticacion
def menu():
    return render_template('menu.html')

# ==================== PERIODOS ====================

@app.route('/periodos', methods=['GET'])
@verificar_autenticacion
def listar_periodos():
    return render_template('periodos/listar_periodos.html')

@app.route('/api/periodos', methods=['GET'])
@verificar_autenticacion
def api_get_periodos():
    try:
        periodos = periodo_service.listar_periodos()
        return jsonify([{
            'nombre': p.nombre,
            'fecha_inicio': p.fecha_inicio.isoformat() if p.fecha_inicio else None,
            'fecha_fin': p.fecha_fin.isoformat() if p.fecha_fin else None,
            'activo': p.activo
        } for p in periodos])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/periodos/crear', methods=['GET', 'POST'])
@verificar_autenticacion
def crear_periodo():
    if request.method == 'POST':
        try:
            nombre = request.form.get('nombre')
            fecha_inicio = request.form.get('fecha_inicio')
            fecha_fin = request.form.get('fecha_fin')
            
            if not nombre:
                return render_template('periodos/crear_periodo.html', error='El nombre del período es requerido')
            
            if fecha_inicio:
                fecha_inicio = datetime.fromisoformat(fecha_inicio).date()
            if fecha_fin:
                fecha_fin = datetime.fromisoformat(fecha_fin).date()
            
            periodo_service.crear_periodo(nombre, fecha_inicio, fecha_fin)
            flash(f'Período {nombre} creado exitosamente', 'success')
            return redirect(url_for('listar_periodos'))
        except Exception as e:
            return render_template('periodos/crear_periodo.html', error=f'Error: {str(e)}')
    
    return render_template('periodos/crear_periodo.html')

@app.route('/api/periodos/<nombre>/activar', methods=['POST'])
@verificar_autenticacion
def api_activar_periodo(nombre):
    try:
        periodo_service.activar_periodo(nombre)
        return jsonify({'mensaje': f'Período {nombre} activado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/periodos/finalizar', methods=['POST'])
@verificar_autenticacion
def api_finalizar_periodo():
    try:
        periodo_finalizado = periodo_service.finalizar_periodo_activo()
        return jsonify({'mensaje': f'Período {periodo_finalizado.nombre} finalizado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/periodos/<nombre>/eliminar', methods=['POST'])
@verificar_autenticacion
def api_eliminar_periodo(nombre):
    try:
        periodo_service.eliminar_periodo(nombre)
        return jsonify({'mensaje': f'Período {nombre} eliminado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ==================== CARRERAS ====================

@app.route('/carreras', methods=['GET', 'POST'])
@verificar_autenticacion
def configurar_carrera():
    if request.method == 'POST':
        try:
            nombre = request.form.get('nombre')
            sigla = request.form.get('sigla')
            cupos = int(request.form.get('cupos', 0))
            
            if not nombre or not sigla or cupos <= 0:
                return render_template('carreras/configurar_carrera.html', error='Todos los campos son requeridos')
            
            # Obtener período activo
            periodo = periodo_service.obtener_periodo_activo()
            if not periodo:
                return render_template('carreras/configurar_carrera.html', error='Debes activar un período antes de registrar carreras')
            
            # Obtener ofertas actuales
            try:
                ofertas = oferta_service.leer_ofertas()
            except:
                ofertas = []
            
            # Crear nueva oferta con todos los parámetros requeridos
            nueva_oferta = OfertaAcademica(
                codigo_carrera=f"CARR-{len(ofertas)+1:03d}",
                institucion="Instituto Estatal",
                provincia="San José",
                canton="San José",
                nombre_carrera=nombre,
                area="Educación",
                nivel="Licenciatura",
                modalidad="Presencial",
                jornada="Diurna",
                tipo_cupo="General",
                total_cupos=cupos,
                periodo=periodo.nombre
            )
            ofertas.append(nueva_oferta)
            
            oferta_service.guardar_ofertas(ofertas)
            flash(f'Carrera {nombre} registrada exitosamente', 'success')
            return redirect(url_for('configurar_carrera'))
        except Exception as e:
            return render_template('carreras/configurar_carrera.html', error=f'Error: {str(e)}')
    
    try:
        ofertas = oferta_service.leer_ofertas()
    except:
        ofertas = []
    
    return render_template('carreras/configurar_carrera.html', ofertas=ofertas)

@app.route('/carreras/cargar', methods=['GET', 'POST'])
@verificar_autenticacion
def cargar_ofertas():
    if request.method == 'POST':
        try:
            archivo = request.files.get('archivo')
            
            if not archivo:
                return render_template('carreras/configurar_carrera.html', error='Debe seleccionar un archivo')
            
            if not allowed_file(archivo.filename):
                return render_template('carreras/configurar_carrera.html', error='Formato no permitido. Use CSV o XLSX')
            
            filename = secure_filename(archivo.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            archivo.save(filepath)
            
            # Procesar archivo
            if filename.endswith('.csv'):
                oferta_service.cargar_desde_csv(filepath)
            elif filename.endswith(('.xlsx', '.xls')):
                # Convertir Excel a CSV temporal
                df = pd.read_excel(filepath)
                csv_temp = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_ofertas.csv')
                df.to_csv(csv_temp, index=False)
                oferta_service.cargar_desde_csv(csv_temp)
                os.remove(csv_temp)
            
            # Limpiar archivo
            os.remove(filepath)
            
            flash('Ofertas académicas cargadas exitosamente', 'success')
            return redirect(url_for('configurar_carrera'))
        except Exception as e:
            return render_template('carreras/configurar_carrera.html', error=f'Error: {str(e)}')

# ==================== OFERTAS ACADÉMICAS ====================

@app.route('/ofertas', methods=['GET'])
@verificar_autenticacion
def ver_ofertas():
    return render_template('ofertas/ver_ofertas.html')

@app.route('/api/ofertas', methods=['GET'])
@verificar_autenticacion
def api_get_ofertas():
    try:
        ofertas = oferta_service.leer_ofertas()
        postulantes = postulante_service.leer_postulantes()
        
        resultado = []
        for oferta in ofertas:
            resultado.append({
                'codigo': oferta.codigo_carrera,
                'nombre': oferta.nombre_carrera,
                'institucion': oferta.institucion,
                'provincia': oferta.provincia,
                'canton': oferta.canton,
                'area': oferta.area,
                'nivel': oferta.nivel,
                'modalidad': oferta.modalidad,
                'jornada': oferta.jornada,
                'tipo_cupo': oferta.tipo_cupo,
                'cupos_totales': oferta.total_cupos,
                'cupos_disponibles': oferta.cupos_disponibles
            })
        
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== POSTULANTES ====================

@app.route('/postulantes/cargar', methods=['GET', 'POST'])
@verificar_autenticacion
def cargar_postulantes():
    if request.method == 'POST':
        try:
            archivo = request.files.get('archivo')
            
            if not archivo:
                return render_template('postulantes/cargar_postulantes.html', error='Debe seleccionar un archivo')
            
            if not allowed_file(archivo.filename):
                return render_template('postulantes/cargar_postulantes.html', error='Formato no permitido. Use CSV o XLSX')
            
            filename = secure_filename(archivo.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            archivo.save(filepath)
            
            # Procesar archivo
            if filename.endswith('.csv'):
                postulante_service.cargar_desde_csv(filepath)
            elif filename.endswith(('.xlsx', '.xls')):
                # Convertir Excel a CSV temporal
                df = pd.read_excel(filepath)
                csv_temp = os.path.join(app.config['UPLOAD_FOLDER'], 'temp.csv')
                df.to_csv(csv_temp, index=False)
                postulante_service.cargar_desde_csv(csv_temp)
                os.remove(csv_temp)
            
            # Limpiar archivo
            os.remove(filepath)
            
            flash('Postulantes cargados exitosamente', 'success')
            return redirect(url_for('menu'))
        except Exception as e:
            return render_template('postulantes/cargar_postulantes.html', error=f'Error: {str(e)}')
    
    return render_template('postulantes/cargar_postulantes.html')

@app.route('/api/postulantes', methods=['GET'])
@verificar_autenticacion
def api_get_postulantes():
    try:
        postulantes = postulante_service.leer_postulantes()
        return jsonify([{
            'id': p.id_postulante,
            'nombre': f"{p.nombres} {p.apellidos}",
            'nota': p.nota_postulacion,
            'opcion_1': p.opcion_1
        } for p in postulantes])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== ASIGNACIÓN ====================

@app.route('/asignacion', methods=['GET', 'POST'])
@verificar_autenticacion
def ejecutar_asignacion():
    if request.method == 'POST':
        try:
            # Validar que existan datos
            try:
                postulantes = postulante_service.leer_postulantes()
                ofertas = oferta_service.leer_ofertas()
            except Exception as e:
                return render_template('resultados/ejecutar_asignacion.html', 
                                     error=f'No hay período activo o datos incompletos: {str(e)}')
            
            if not postulantes:
                return render_template('resultados/ejecutar_asignacion.html', 
                                     error='No hay postulantes cargados')
            if not ofertas:
                return render_template('resultados/ejecutar_asignacion.html', 
                                     error='No hay ofertas académicas cargadas')
            
            # Ejecutar asignación
            try:
                asignacion_service.ejecutar_asignacion()
            except Exception as e:
                print(f"Error en asignación: {str(e)}")
                import traceback
                print(traceback.format_exc())
                return render_template('resultados/ejecutar_asignacion.html', 
                                     error=f'Error durante la asignación: {str(e)}')
            
            flash('Asignación ejecutada exitosamente', 'success')
            return redirect(url_for('ver_resultados'))
        except Exception as e:
            print(f"Error general: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return render_template('resultados/ejecutar_asignacion.html', 
                                 error=f'Error: {str(e)}')
    
    return render_template('resultados/ejecutar_asignacion.html')

# ==================== RESULTADOS ====================

@app.route('/resultados', methods=['GET'])
@verificar_autenticacion
def ver_resultados():
    return render_template('resultados/ver_resultados.html')

@app.route('/api/resultados', methods=['GET'])
@verificar_autenticacion
def api_get_resultados():
    try:
        ruta = periodo_service.obtener_ruta_periodo_activo()
        archivo = f"{ruta}/resultados_asignacion.json"
        
        if not os.path.exists(archivo):
            return jsonify([])
        
        with open(archivo, 'r', encoding='utf-8') as f:
            resultados = json.load(f)
        
        return jsonify(resultados)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/resultados/exportar', methods=['GET', 'POST'])
@verificar_autenticacion
def exportar_resultados():
    if request.method == 'POST':
        try:
            formato = request.form.get('formato', 'xlsx')
            
            # Leer resultados
            ruta = periodo_service.obtener_ruta_periodo_activo()
            archivo = f"{ruta}/resultados_asignacion.json"
            
            if not os.path.exists(archivo):
                flash('No hay resultados para exportar', 'warning')
                return redirect(url_for('ver_resultados'))
            
            with open(archivo, 'r', encoding='utf-8') as f:
                resultados = json.load(f)
            
            if formato == 'csv':
                # Crear CSV
                output = io.StringIO()
                if resultados:
                    writer = csv.DictWriter(output, fieldnames=resultados[0].keys())
                    writer.writeheader()
                    writer.writerows(resultados)
                
                output.seek(0)
                return send_file(
                    io.BytesIO(output.getvalue().encode()),
                    mimetype='text/csv',
                    as_attachment=True,
                    download_name='resultados_asignacion.csv'
                )
            
            elif formato == 'xlsx':
                # Crear Excel
                df = pd.DataFrame(resultados)
                output = io.BytesIO()
                df.to_excel(output, index=False, sheet_name='Resultados')
                output.seek(0)
                
                return send_file(
                    output,
                    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    as_attachment=True,
                    download_name='resultados_asignacion.xlsx'
                )
            
            else:
                flash('Formato no soportado', 'error')
                return redirect(url_for('ver_resultados'))
        
        except Exception as e:
            flash(f'Error al exportar: {str(e)}', 'error')
            return redirect(url_for('ver_resultados'))
    
    return render_template('resultados/exportar_resultados.html')

# ==================== ESTADÍSTICAS ====================

@app.route('/estadisticas', methods=['GET'])
@verificar_autenticacion
def ver_estadisticas():
    return render_template('estadisticas/ver_estadisticas.html')

@app.route('/api/estadisticas', methods=['GET'])
@verificar_autenticacion
def api_get_estadisticas():
    try:
        ruta = periodo_service.obtener_ruta_periodo_activo()
        archivo = f"{ruta}/resultados_asignacion.json"
        
        if not os.path.exists(archivo):
            return jsonify({
                'total': 0,
                'asignados': 0,
                'no_asignados': 0,
                'porcentaje': 0,
                'por_carrera': {}
            })
        
        with open(archivo, 'r', encoding='utf-8') as f:
            resultados = json.load(f)
        
        total = len(resultados)
        asignados = [r for r in resultados if r.get('estado_asignacion') == 'ASIGNADO']
        no_asignados = total - len(asignados)
        porcentaje = (len(asignados) / total * 100) if total > 0 else 0
        
        # Conteo por carrera
        carreras = Counter(
            r.get('carrera') for r in asignados if r.get('carrera') is not None
        )
        
        return jsonify({
            'total': total,
            'asignados': len(asignados),
            'no_asignados': no_asignados,
            'porcentaje': round(porcentaje, 2),
            'por_carrera': dict(carreras)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== MANEJO DE ERRORES ====================

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', mensaje='Página no encontrada'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('error.html', mensaje='Error interno del servidor'), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
