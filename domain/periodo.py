# domain/periodo.py

class Periodo:
    def __init__(self,
        id_periodo,
        nombre,
        activo=False):
        
        self.id_periodo = id_periodo
        self.nombre = nombre
        self.activo = activo

    def activar(self):
        self.activo = True

    def cerrar(self):
        self.activo = False
