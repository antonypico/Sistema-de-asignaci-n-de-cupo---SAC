# patterns/strategy/segmento_asignacion_strategy.py

from abc import ABC, abstractmethod


class SegmentoAsignacionStrategy(ABC):

    def __init__(self, nombre_segmento, porcentaje_cupos):
        self.nombre_segmento = nombre_segmento
        self.porcentaje_cupos = porcentaje_cupos

    def calcular_cupos(self, total_cupos):
        """
        Calcula los cupos del segmento según el porcentaje definido
        """
        return int(total_cupos * self.porcentaje_cupos)

    @abstractmethod
    def asignar(self, estudiantes, ofertas):
        pass
