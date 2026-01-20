from enum import Enum
from datetime import datetime


class TipoDesempate(Enum):
    """Tipos predefinidos de criterios de desempate"""
    MAYOR_EDAD = "mayor_edad"  # Quien sea más mayor
    MENOR_EDAD = "menor_edad"  # Quien sea más joven
    ALFABETICO_APELLIDO = "alfabetico_apellido"  # A-Z por apellido
    ALFABETICO_NOMBRE = "alfabetico_nombre"  # A-Z por nombre
    FECHA_INSCRIPCION = "fecha_inscripcion"  # Por fecha de inscripción
    MANUAL = "manual"  # Cambios manuales del administrador


class CriterioDesempate:
    """Clase que representa un criterio de desempate para un segmento"""
    
    def __init__(self, segmento_nombre, tipo_desempate=TipoDesempate.ALFABETICO_APELLIDO):
        self.segmento_nombre = segmento_nombre
        self.tipo_desempate = tipo_desempate
        # Mapeo de postulante_id -> posición manual (si aplica)
        self.ordenamiento_manual = {}
        self.fecha_actualizacion = datetime.now()
    
    def aplicar_desempate(self, estudiantes_empatados):
        """
        Aplica el criterio de desempate a un grupo de estudiantes con la misma nota
        
        Args:
            estudiantes_empatados: Lista de estudiantes con misma nota y segmento
            
        Returns:
            Lista ordenada de estudiantes según el criterio
        """
        if not estudiantes_empatados:
            return []
        
        # Si hay ordenamiento manual, aplicarlo primero
        if self.ordenamiento_manual:
            return self._aplicar_ordenamiento_manual(estudiantes_empatados)
        
        # Si no, aplicar criterio automático
        return self._aplicar_criterio_automatico(estudiantes_empatados)
    
    def _aplicar_ordenamiento_manual(self, estudiantes):
        """Ordena según el mapeo manual del administrador"""
        estudiantes_con_posicion = []
        
        for est in estudiantes:
            posicion = self.ordenamiento_manual.get(est.id_postulante, float('inf'))
            estudiantes_con_posicion.append((posicion, est))
        
        # Ordenar por posición manual, luego por criterio automático para los no definidos
        estudiantes_con_posicion.sort(key=lambda x: (x[0], self._clave_criterio_automatico(x[1])))
        return [est for _, est in estudiantes_con_posicion]
    
    def _aplicar_criterio_automatico(self, estudiantes):
        """Aplica el criterio automático seleccionado"""
        if self.tipo_desempate == TipoDesempate.ALFABETICO_APELLIDO:
            return sorted(estudiantes, key=lambda e: (e.apellidos.lower(), e.nombres.lower()))
        
        elif self.tipo_desempate == TipoDesempate.ALFABETICO_NOMBRE:
            return sorted(estudiantes, key=lambda e: (e.nombres.lower(), e.apellidos.lower()))
        
        elif self.tipo_desempate == TipoDesempate.MAYOR_EDAD:
            # Requiere fecha_nacimiento en el estudiante
            return sorted(estudiantes, key=lambda e: getattr(e, 'fecha_nacimiento', datetime.now()), reverse=False)
        
        elif self.tipo_desempate == TipoDesempate.MENOR_EDAD:
            return sorted(estudiantes, key=lambda e: getattr(e, 'fecha_nacimiento', datetime.now()), reverse=True)
        
        elif self.tipo_desempate == TipoDesempate.FECHA_INSCRIPCION:
            # Requiere fecha_inscripcion en el estudiante
            return sorted(estudiantes, key=lambda e: getattr(e, 'fecha_inscripcion', datetime.now()))
        
        else:
            # Por defecto, ordenar alfabéticamente por apellido
            return sorted(estudiantes, key=lambda e: (e.apellidos.lower(), e.nombres.lower()))
    
    def _clave_criterio_automatico(self, estudiante):
        """Genera la clave de ordenamiento para un criterio automático"""
        if self.tipo_desempate == TipoDesempate.ALFABETICO_APELLIDO:
            return (estudiante.apellidos.lower(), estudiante.nombres.lower())
        elif self.tipo_desempate == TipoDesempate.ALFABETICO_NOMBRE:
            return (estudiante.nombres.lower(), estudiante.apellidos.lower())
        elif self.tipo_desempate == TipoDesempate.MAYOR_EDAD:
            return getattr(estudiante, 'fecha_nacimiento', datetime.now())
        elif self.tipo_desempate == TipoDesempate.MENOR_EDAD:
            return -getattr(estudiante, 'fecha_nacimiento', datetime.now()).timestamp()
        else:
            return (estudiante.apellidos.lower(), estudiante.nombres.lower())
    
    def establecer_ordenamiento_manual(self, lista_postulante_ids):
        """
        Establece el ordenamiento manual de postulantes
        
        Args:
            lista_postulante_ids: Lista ordenada de IDs de postulantes
        """
        self.ordenamiento_manual = {
            postulante_id: posicion 
            for posicion, postulante_id in enumerate(lista_postulante_ids)
        }
        self.tipo_desempate = TipoDesempate.MANUAL
        self.fecha_actualizacion = datetime.now()
    
    def agregar_cambio_manual(self, postulante_id, posicion):
        """Agrega o modifica un cambio manual para un postulante específico"""
        self.ordenamiento_manual[postulante_id] = posicion
        self.tipo_desempate = TipoDesempate.MANUAL
        self.fecha_actualizacion = datetime.now()
    
    def remover_cambio_manual(self, postulante_id):
        """Remueve un cambio manual para un postulante"""
        if postulante_id in self.ordenamiento_manual:
            del self.ordenamiento_manual[postulante_id]
    
    def obtener_cambios_manuales(self):
        """Retorna el diccionario de cambios manuales"""
        return self.ordenamiento_manual.copy()
    
    def cambiar_criterio(self, nuevo_tipo_desempate):
        """Cambia el criterio automático de desempate"""
        if isinstance(nuevo_tipo_desempate, TipoDesempate):
            self.tipo_desempate = nuevo_tipo_desempate
        else:
            self.tipo_desempate = TipoDesempate(nuevo_tipo_desempate)
        self.fecha_actualizacion = datetime.now()
    
    def resetear_ordenamiento_manual(self):
        """Limpia todos los cambios manuales"""
        self.ordenamiento_manual = {}
        self.fecha_actualizacion = datetime.now()
    
    def to_dict(self):
        """Convierte el criterio a diccionario para persistencia"""
        return {
            'segmento_nombre': self.segmento_nombre,
            'tipo_desempate': self.tipo_desempate.value,
            'ordenamiento_manual': self.ordenamiento_manual,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat()
        }
    
    @staticmethod
    def from_dict(data):
        """Crea un criterio desde un diccionario"""
        criterio = CriterioDesempate(
            data['segmento_nombre'],
            TipoDesempate(data.get('tipo_desempate', TipoDesempate.ALFABETICO_APELLIDO.value))
        )
        # Convertir las posiciones a int si están guardadas como strings
        ordenamiento_manual = data.get('ordenamiento_manual', {})
        criterio.ordenamiento_manual = {
            k: int(v) if isinstance(v, str) else v 
            for k, v in ordenamiento_manual.items()
        }
        return criterio
