import json
from pathlib import Path
from domain.criterio_desempate import CriterioDesempate, TipoDesempate


class DesempateService:
    """Servicio para gestionar criterios de desempate en la asignación de cupos"""
    
    def __init__(self, archivo_config_desempates="data/criterios_desempate.json"):
        self.archivo_config = archivo_config_desempates
        self.criterios = {}  # {segmento_nombre: CriterioDesempate}
        self._inicializar_criterios()
    
    def _inicializar_criterios(self):
        """Carga los criterios de desempate desde archivo o crea los predefinidos"""
        if Path(self.archivo_config).exists():
            self._cargar_criterios_desde_archivo()
        else:
            self._crear_criterios_predefinidos()
    
    def _crear_criterios_predefinidos(self):
        """Crea los criterios predefinidos para cada segmento"""
        segmentos = [
            "Política de Cuotas",
            "Vulnerabilidad",
            "Mérito Académico",
            "Otros Méritos",
            "Bachilleres Pueblos Nacionalidades",
            "Bachilleres Generales",
            "Población General"
        ]
        
        for segmento in segmentos:
            self.criterios[segmento] = CriterioDesempate(
                segmento,
                TipoDesempate.ALFABETICO_APELLIDO
            )
        
        self._guardar_criterios()
    
    def _cargar_criterios_desde_archivo(self):
        """Carga los criterios desde el archivo JSON"""
        try:
            with open(self.archivo_config, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for segmento, criterio_data in data.items():
                    self.criterios[segmento] = CriterioDesempate.from_dict(criterio_data)
        except Exception as e:
            print(f"Error al cargar criterios: {e}")
            self._crear_criterios_predefinidos()
    
    def _guardar_criterios(self):
        """Persiste los criterios en archivo JSON"""
        try:
            Path(self.archivo_config).parent.mkdir(parents=True, exist_ok=True)
            data = {
                segmento: criterio.to_dict()
                for segmento, criterio in self.criterios.items()
            }
            with open(self.archivo_config, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar criterios: {e}")
    
    def obtener_criterio(self, segmento_nombre):
        """Obtiene el criterio de desempate para un segmento"""
        return self.criterios.get(segmento_nombre)
    
    def obtener_todos_criterios(self):
        """Retorna todos los criterios de desempate"""
        return self.criterios.copy()
    
    def establecer_criterio_automatico(self, segmento_nombre, tipo_desempate):
        """
        Cambia el criterio automático de desempate para un segmento
        
        Args:
            segmento_nombre: Nombre del segmento
            tipo_desempate: TipoDesempate enum o string
        """
        if segmento_nombre not in self.criterios:
            self.criterios[segmento_nombre] = CriterioDesempate(segmento_nombre)
        
        self.criterios[segmento_nombre].cambiar_criterio(tipo_desempate)
        self._guardar_criterios()
    
    def establecer_ordenamiento_manual(self, segmento_nombre, lista_postulante_ids):
        """
        Establece un ordenamiento manual para un segmento
        
        Args:
            segmento_nombre: Nombre del segmento
            lista_postulante_ids: Lista ordenada de IDs de postulantes
        """
        if segmento_nombre not in self.criterios:
            self.criterios[segmento_nombre] = CriterioDesempate(segmento_nombre)
        
        self.criterios[segmento_nombre].establecer_ordenamiento_manual(lista_postulante_ids)
        self._guardar_criterios()
    
    def agregar_cambio_manual(self, segmento_nombre, postulante_id, posicion):
        """Agrega un cambio manual para un postulante en un segmento"""
        if segmento_nombre not in self.criterios:
            self.criterios[segmento_nombre] = CriterioDesempate(segmento_nombre)
        
        self.criterios[segmento_nombre].agregar_cambio_manual(postulante_id, posicion)
        self._guardar_criterios()
    
    def remover_cambio_manual(self, segmento_nombre, postulante_id):
        """Remueve un cambio manual para un postulante"""
        if segmento_nombre in self.criterios:
            self.criterios[segmento_nombre].remover_cambio_manual(postulante_id)
            self._guardar_criterios()
    
    def resetear_ordenamiento_manual(self, segmento_nombre):
        """Limpia todos los cambios manuales de un segmento"""
        if segmento_nombre in self.criterios:
            self.criterios[segmento_nombre].resetear_ordenamiento_manual()
            self._guardar_criterios()
    
    def aplicar_desempate(self, segmento_nombre, estudiantes_empatados):
        """
        Aplica el criterio de desempate a un grupo de estudiantes
        
        Args:
            segmento_nombre: Nombre del segmento
            estudiantes_empatados: Lista de estudiantes con misma nota
            
        Returns:
            Lista ordenada de estudiantes
        """
        criterio = self.obtener_criterio(segmento_nombre)
        if criterio:
            return criterio.aplicar_desempate(estudiantes_empatados)
        else:
            # Si no existe criterio, retornar ordenado alfabéticamente
            return sorted(estudiantes_empatados, key=lambda e: (e.apellidos.lower(), e.nombres.lower()))
    
    def obtener_tipo_desempate(self, segmento_nombre):
        """Obtiene el tipo de desempate actualmente configurado"""
        criterio = self.obtener_criterio(segmento_nombre)
        if criterio:
            return criterio.tipo_desempate.value
        return None
    
    def obtener_cambios_manuales(self, segmento_nombre):
        """Obtiene los cambios manuales de un segmento"""
        criterio = self.obtener_criterio(segmento_nombre)
        if criterio:
            return criterio.obtener_cambios_manuales()
        return {}
    
    def obtener_opciones_desempate(self):
        """Retorna las opciones disponibles de desempate"""
        return [
            {
                'valor': TipoDesempate.ALFABETICO_APELLIDO.value,
                'etiqueta': 'Alfabético por Apellido (A-Z)',
                'descripcion': 'Ordena de forma alfabética por apellido'
            },
            {
                'valor': TipoDesempate.ALFABETICO_NOMBRE.value,
                'etiqueta': 'Alfabético por Nombre (A-Z)',
                'descripcion': 'Ordena de forma alfabética por nombre'
            },
            {
                'valor': TipoDesempate.MAYOR_EDAD.value,
                'etiqueta': 'Mayor Edad',
                'descripcion': 'Favorece a los estudiantes más mayores'
            },
            {
                'valor': TipoDesempate.MENOR_EDAD.value,
                'etiqueta': 'Menor Edad',
                'descripcion': 'Favorece a los estudiantes más jóvenes'
            },
            {
                'valor': TipoDesempate.FECHA_INSCRIPCION.value,
                'etiqueta': 'Fecha de Inscripción',
                'descripcion': 'Por orden de inscripción (primero quien se inscribió primero)'
            },
        ]
