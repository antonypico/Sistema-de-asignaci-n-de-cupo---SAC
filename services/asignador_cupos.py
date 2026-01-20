# services/asignador_cupos.py

from patterns.strategy.segmento_politica_cuotas import SegmentoPoliticaCuotas
from patterns.strategy.segmento_vulnerabilidad import SegmentoVulnerabilidad
from patterns.strategy.segmento_merito_academico import SegmentoMeritoAcademico
from patterns.strategy.segmento_otros_meritos import SegmentoOtrosMeritos
from patterns.strategy.segmento_bachilleres_pueblos import SegmentoBachillerPN
from patterns.strategy.segmento_bachilleres_generales import SegmentoBachillerGeneral
from patterns.strategy.segmento_poblacion_general import SegmentoPoblacionGeneral

from domain.resultado_asignacion import ResultadoAsignacion
from services.desempate_service import DesempateService


class AsignadorCupos:
    def __init__(self, estudiantes, ofertas, desempate_service=None):
        self.estudiantes = estudiantes
        self.ofertas = ofertas
        
        # Inicializar servicio de desempate si no se proporciona
        self.desempate_service = desempate_service or DesempateService()
        
        # Calcular cupos totales disponibles
        self.cupos_totales_disponibles = sum(oferta.cupos_disponibles for oferta in ofertas)
        self.cupos_asignados = 0

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
        
        # Inyectar el servicio de desempate en cada segmento
        for segmento in self.segmentos:
            segmento.establecer_desempate_service(self.desempate_service)

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
        asignados = 0
        for estudiante in self.estudiantes:
            if estudiante.esta_asignado():
                asignados += 1
            resultados.append(ResultadoAsignacion(estudiante))
        
        # Validación: contar cupos totales consumidos
        cupos_consumidos = sum(oferta.total_cupos - oferta.cupos_disponibles for oferta in self.ofertas)
        
        print(f"[ASIGNADOR] Cupos consumidos: {cupos_consumidos}")
        print(f"[ASIGNADOR] Estudiantes asignados: {asignados}")
        
        # Validación: si asignados > cupos_consumidos, hay un problema
        if asignados != cupos_consumidos:
            print(f"[ADVERTENCIA] Discrepancia: {asignados} asignados pero {cupos_consumidos} cupos consumidos")
        
        return resultados
