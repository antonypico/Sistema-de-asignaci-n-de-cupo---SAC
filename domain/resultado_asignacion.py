# domain/resultado_asignacion.py

class ResultadoAsignacion:
    def __init__(self, estudiante):
        self.id_estudiante = estudiante.id_estudiante
        self.nombre = estudiante.nombre_completo()
        self.carrera_asignada = (
            estudiante.oferta_asignada.carrera.nombre
            if estudiante.oferta_asignada
            else "NO ASIGNADO"
        )
