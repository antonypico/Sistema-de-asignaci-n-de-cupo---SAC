from patterns.strategy.segmento_asignacion_strategy import SegmentoAsignacionStrategy


class SegmentoPoliticaCuotas(SegmentoAsignacionStrategy):

    def __init__(self):
        super().__init__(
            nombre_segmento="Política de Cuotas",
            porcentaje_cupos=0.10
        )

    def asignar(self, estudiantes, ofertas):
        asignados = []
        no_asignados = []
        cupos_no_usados = 0

        postulantes = [
            e for e in estudiantes
            if e.es_politica_cuotas and not e.esta_asignado()
        ]

        postulantes.sort(key=lambda e: e.nota_postulacion, reverse=True)

        for estudiante in postulantes:
            # Si perdió desempate, no intentar asignarlo
            if hasattr(estudiante, 'perdio_desempate') and estudiante.perdio_desempate:
                no_asignados.append(estudiante)
                continue
            
            for opcion in estudiante.opciones_carrera:
                oferta = self._buscar_oferta(opcion, ofertas)
                if oferta:
                    oferta.consumir_cupo()
                    estudiante.marcar_asignado(oferta)
                    asignados.append(estudiante)
                    break
            else:
                no_asignados.append(estudiante)

        return asignados, no_asignados, cupos_no_usados



