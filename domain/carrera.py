# domain/carrera.py

class Carrera:
    def __init__(
        self,
        nombre,
        area,
        subarea,
        nivel,
        modalidad,
        jornada,
        institucion
    ):
        self.nombre = nombre
        self.area = area
        self.subarea = subarea
        self.nivel = nivel
        self.modalidad = modalidad
        self.jornada = jornada
        self.institucion = institucion

