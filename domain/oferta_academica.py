# domain/oferta_academica.py

class OfertaAcademica:
    def __init__(self, carrera, total_cupos):
        self.carrera = carrera
        self.total_cupos = total_cupos
        self.cupos_disponibles = total_cupos

    def tiene_cupos(self):
        return self.cupos_disponibles > 0

    def consumir_cupo(self):
        if self.cupos_disponibles <= 0:
            raise ValueError("No hay cupos disponibles")
        self.cupos_disponibles -= 1