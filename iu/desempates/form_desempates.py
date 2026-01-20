from iu.base.ventana_base import VentanaBase


class FormDesempates(VentanaBase):
    """Formulario para gestionar criterios de desempate entre postulantes"""
    
    def __init__(self, desempate_service, periodo_actual):
        super().__init__()
        self.desempate_service = desempate_service
        self.periodo_actual = periodo_actual
        self.segmento_seleccionado = None
        self.estudiantes_empatados = []
        
        self.inicializar_ui()
    
    def inicializar_ui(self):
        """Inicializa los componentes de la interfaz"""
        # Aquí irá el código para crear la UI
        # Este es un esqueleto base
        pass
    
    def cargar_segmentos(self):
        """Carga los segmentos disponibles"""
        return list(self.desempate_service.obtener_todos_criterios().keys())
    
    def obtener_criterio_segmento(self, segmento_nombre):
        """Obtiene el criterio de desempate para un segmento"""
        return self.desempate_service.obtener_criterio(segmento_nombre)
    
    def cambiar_criterio(self, segmento_nombre, tipo_desempate):
        """Cambia el criterio de desempate para un segmento"""
        self.desempate_service.establecer_criterio_automatico(segmento_nombre, tipo_desempate)
    
    def obtener_opciones_desempate(self):
        """Obtiene las opciones disponibles de desempate"""
        return self.desempate_service.obtener_opciones_desempate()
    
    def aplicar_ordenamiento_manual(self, segmento_nombre, lista_ids_ordenados):
        """Aplica un ordenamiento manual de postulantes"""
        self.desempate_service.establecer_ordenamiento_manual(segmento_nombre, lista_ids_ordenados)
    
    def obtener_cambios_manuales(self, segmento_nombre):
        """Obtiene los cambios manuales para un segmento"""
        return self.desempate_service.obtener_cambios_manuales(segmento_nombre)
    
    def resetear_ordenamiento_manual(self, segmento_nombre):
        """Limpia los cambios manuales de un segmento"""
        self.desempate_service.resetear_ordenamiento_manual(segmento_nombre)
