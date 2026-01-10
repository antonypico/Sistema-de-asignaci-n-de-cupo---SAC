# domain/estudiante.py

class Estudiante:
    def __init__(
        self,
        id_estudiante,
        nombres,
        apellidos,
        nota_postulacion,
        opciones_carrera,
        es_cuadro_honor=False,
        tiene_otro_merito=False,
        es_vulnerable=False,
        es_politica_cuotas=False,
        es_pueblo_nacionalidad=False,
        tiene_titulo_superior=False
    ):
        # Identificación
        self.id_estudiante = id_estudiante
        self.nombres = nombres
        self.apellidos = apellidos

        # Mérito académico
        self.nota_postulacion = float(nota_postulacion)
        self.es_cuadro_honor = es_cuadro_honor
        self.tiene_otro_merito = tiene_otro_merito

        # Condiciones sociales / grupos
        self.es_vulnerable = es_vulnerable
        self.es_politica_cuotas = es_politica_cuotas
        self.es_pueblo_nacionalidad = es_pueblo_nacionalidad

        # Restricciones
        self.tiene_titulo_superior = tiene_titulo_superior

        # Postulación
        self.opciones_carrera = opciones_carrera  # lista ordenada de preferencias

        # Estado de asignación
        self.oferta_asignada = None

    # =========================
    # MÉTODOS DE ESTADO
    # =========================

    def esta_asignado(self):
        return self.oferta_asignada is not None

    def marcar_asignado(self, oferta):
        self.oferta_asignada = oferta

    # =========================
    # MÉTODOS AUXILIARES
    # =========================

    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"

