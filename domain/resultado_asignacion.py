class ResultadoAsignacion:
    def __init__(self, estudiante):
        # Referencia al estudiante
        self.estudiante = estudiante

        # Identificación
        self.id_postulante = estudiante.id_postulante
        self.nombre = estudiante.nombre_completo()
        self.segmento = estudiante.obtener_segmento()

        # Resultado de asignación
        if estudiante.oferta_asignada:
            self.carrera_asignada = estudiante.oferta_asignada.carrera.nombre
            self.resultado = "ASIGNADO"
            self.jornada = estudiante.oferta_asignada.jornada
            self.modalidad = estudiante.oferta_asignada.modalidad
            self.razon_no_asignacion = None
            self.gano_desempate = False  # Se actualiza si fue desempatado
            self.perdio_desempate = False  # Se marca si perdió desempate
        else:
            self.carrera_asignada = "NO ASIGNADO"
            self.resultado = "NO ASIGNADO"
            self.jornada = "-"
            self.modalidad = "-"
            self.razon_no_asignacion = self._determinar_razon_no_asignacion(estudiante)
            self.gano_desempate = False
            self.perdio_desempate = False

    def _determinar_razon_no_asignacion(self, estudiante):
        """Determina por qué no se asignó el estudiante"""
        if not estudiante.opciones_carrera:
            return "Sin opciones de carrera registradas"
        
        # Si llegó hasta aquí sin asignación, es porque:
        # 1. No había cupos disponibles, o
        # 2. Sus opciones se agotaron
        return "No había cupos disponibles en sus opciones de carrera"