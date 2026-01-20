"""
API REST para gestionar criterios de desempate
"""
from flask import Blueprint, request, jsonify
from services.desempate_service import DesempateService
from domain.criterio_desempate import TipoDesempate

desempate_bp = Blueprint('desempate', __name__, url_prefix='/api/desempate')

# Instancia global del servicio
_desempate_service = None


def init_desempate_service(desempate_service):
    """Inicializa el servicio de desempate"""
    global _desempate_service
    _desempate_service = desempate_service


@desempate_bp.route('/opciones', methods=['GET'])
def obtener_opciones_desempate():
    """Obtiene las opciones disponibles de desempate"""
    try:
        opciones = _desempate_service.obtener_opciones_desempate()
        return jsonify({
            'success': True,
            'opciones': opciones
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@desempate_bp.route('/criterios', methods=['GET'])
def obtener_todos_criterios():
    """Obtiene todos los criterios de desempate"""
    try:
        criterios = _desempate_service.obtener_todos_criterios()
        resultado = {}
        for segmento, criterio in criterios.items():
            resultado[segmento] = {
                'tipo': criterio.tipo_desempate.value,
                'cambios_manuales': criterio.obtener_cambios_manuales()
            }
        return jsonify({
            'success': True,
            'criterios': resultado
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@desempate_bp.route('/criterio/<segmento_nombre>', methods=['GET'])
def obtener_criterio(segmento_nombre):
    """Obtiene el criterio de desempate para un segmento"""
    try:
        criterio = _desempate_service.obtener_criterio(segmento_nombre)
        if not criterio:
            return jsonify({
                'success': False,
                'error': f'Segmento {segmento_nombre} no encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'criterio': {
                'segmento': segmento_nombre,
                'tipo': criterio.tipo_desempate.value,
                'cambios_manuales': criterio.obtener_cambios_manuales()
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@desempate_bp.route('/criterio/<segmento_nombre>', methods=['PUT'])
def actualizar_criterio(segmento_nombre):
    """Actualiza el criterio de desempate para un segmento"""
    try:
        data = request.get_json()
        tipo_desempate = data.get('tipo_desempate')
        
        if not tipo_desempate:
            return jsonify({
                'success': False,
                'error': 'tipo_desempate es requerido'
            }), 400
        
        _desempate_service.establecer_criterio_automatico(segmento_nombre, tipo_desempate)
        
        return jsonify({
            'success': True,
            'mensaje': f'Criterio actualizado para {segmento_nombre}'
        }), 200
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': f'Tipo de desempate inválido: {str(e)}'
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@desempate_bp.route('/ordenamiento-manual/<segmento_nombre>', methods=['POST'])
def establecer_ordenamiento_manual(segmento_nombre):
    """Establece un ordenamiento manual para un segmento"""
    try:
        data = request.get_json()
        lista_ids = data.get('lista_ids')
        
        if not lista_ids or not isinstance(lista_ids, list):
            return jsonify({
                'success': False,
                'error': 'lista_ids es requerido y debe ser una lista'
            }), 400
        
        _desempate_service.establecer_ordenamiento_manual(segmento_nombre, lista_ids)
        
        return jsonify({
            'success': True,
            'mensaje': f'Ordenamiento manual establecido para {segmento_nombre}'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@desempate_bp.route('/cambio-manual/<segmento_nombre>', methods=['POST'])
def agregar_cambio_manual(segmento_nombre):
    """Agrega un cambio manual para un postulante específico"""
    try:
        data = request.get_json()
        postulante_id = data.get('postulante_id')
        posicion = data.get('posicion')
        
        if not postulante_id or posicion is None:
            return jsonify({
                'success': False,
                'error': 'postulante_id y posicion son requeridos'
            }), 400
        
        _desempate_service.agregar_cambio_manual(segmento_nombre, postulante_id, int(posicion))
        
        return jsonify({
            'success': True,
            'mensaje': f'Cambio manual agregado para {segmento_nombre}'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@desempate_bp.route('/cambio-manual/<segmento_nombre>/<postulante_id>', methods=['DELETE'])
def remover_cambio_manual(segmento_nombre, postulante_id):
    """Remueve un cambio manual para un postulante"""
    try:
        _desempate_service.remover_cambio_manual(segmento_nombre, postulante_id)
        
        return jsonify({
            'success': True,
            'mensaje': f'Cambio manual removido para {segmento_nombre}'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@desempate_bp.route('/resetear/<segmento_nombre>', methods=['POST'])
def resetear_ordenamiento(segmento_nombre):
    """Limpia todos los cambios manuales de un segmento"""
    try:
        _desempate_service.resetear_ordenamiento_manual(segmento_nombre)
        
        return jsonify({
            'success': True,
            'mensaje': f'Ordenamiento manual reseteado para {segmento_nombre}'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
