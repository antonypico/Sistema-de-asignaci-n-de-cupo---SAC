class ResultadoAsignacion:
    def __init__(self, estudiante):
        # Referencia al estudiante
        self.estudiante = estudiante

        # Identificación
        self.id_postulante = estudiante.id_postulante
        self.nombre = estudiante.nombre_completo()

        # Resultado de asignación
        if estudiante.oferta_asignada:
            self.carrera_asignada = estudiante.oferta_asignada.carrera.nombre
            self.resultado = "ASIGNADO"
        else:
            self.carrera_asignada = "NO ASIGNADO"
            self.resultado = "NO ASIGNADO"