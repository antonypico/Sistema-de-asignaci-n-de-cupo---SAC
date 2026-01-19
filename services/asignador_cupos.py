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
            SegmentoPoblacionGeneral(),
        ]

    def ejecutar(self):
        """
        Ejecuta todos los segmentos sobre la MISMA lista de estudiantes.
        Cada segmento asigna cupos solo a estudiantes NO asignados.
        """
        try:
            for segmento in self.segmentos:
                try:
                    segmento.asignar(
                        self.estudiantes,
                        self.ofertas
                    )
                except Exception as e:
                    print(f"Error en segmento {segmento.__class__.__name__}: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    raise
        except Exception as e:
            print(f"Error fatal en asignación: {str(e)}")
            import traceback
            traceback.print_exc()
            raise

        return self._generar_resultados()

    def _generar_resultados(self):
        resultados = []
        for estudiante in self.estudiantes:
            resultados.append(ResultadoAsignacion(estudiante))
        return resultados
