# services/asignador_cupos.py

from patterns.strategy.segmento_politica_cuotas import SegmentoPoliticaCuotas
from patterns.strategy.segmento_vulnerabilidad import SegmentoVulnerabilidad
from patterns.strategy.segmento_merito_academico import SegmentoMeritoAcademico
from patterns.strategy.segmento_otros_meritos import SegmentoOtrosMeritos
from patterns.strategy.segmento_bachilleres_pueblos import SegmentoBachillerPN
from patterns.strategy.segmento_bachilleres_generales import SegmentoBachillerGeneral
from patterns.strategy.segmento_poblacion_general import SegmentoPoblacionGeneral

from domain.resultado_asignacion import ResultadoAsignacion


class AsignadorCupos:
    def __init__(self, estudiantes, ofertas):
        self.estudiantes = estudiantes
        self.ofertas = ofertas

        # Orden OBLIGATORIO según reglamento
        self.segmentos = [
            SegmentoPoliticaCuotas(),
            SegmentoVulnerabilidad(),
            SegmentoMeritoAcademico(),
            SegmentoOtrosMeritos(),
            SegmentoBachillerPN(),
            SegmentoBachillerGeneral(),
            SegmentoPoblacionGeneral(),  # ← ya entra en el mismo flujo
        ]

    def ejecutar(self):
        estudiantes_restantes = self.estudiantes[:]

        # Ejecutar TODOS los segmentos en orden
        for segmento in self.segmentos:
            asignados, no_asignados, _ = segmento.asignar(
                estudiantes_restantes,
                self.ofertas
            )

            # Los no asignados pasan al siguiente segmento
            estudiantes_restantes = no_asignados

        return self._generar_resultados()

    def _generar_resultados(self):
        resultados = []
        for estudiante in self.estudiantes:
            resultados.append(ResultadoAsignacion(estudiante))
        return resultados

