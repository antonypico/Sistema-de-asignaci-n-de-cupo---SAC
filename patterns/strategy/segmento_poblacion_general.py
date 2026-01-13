from patterns.strategy.segmento_asignacion_strategy import SegmentoAsignacionStrategy


class SegmentoPoblacionGeneral(SegmentoAsignacionStrategy):

    def __init__(self):
        super().__init__(
            nombre_segmento="Población General",
            porcentaje_cupos=0.20
        )

    def asignar(self, estudiantes, ofertas):
        asignados = []
        no_asignados = []
        cupos_no_usados = 0  # se mantiene por contrato

        # Todos los estudiantes que aún no han sido asignados
        postulantes = [
            e for e in estudiantes
            if not e.esta_asignado()
        ]

        # Orden por nota (meritocracia)
        postulantes.sort(key=lambda e: e.nota_postulacion, reverse=True)

        for estudiante in postulantes:
            for opcion in estudiante.opciones_carrera:
                oferta = next(
                    (
                        o for o in ofertas
                        if o.codigo_carrera == opcion and o.tiene_cupos()
                    ),
                    None
                )

                if oferta:
                    oferta.consumir_cupo()
                    estudiante.marcar_asignado(oferta)
                    asignados.append(estudiante)
                    break
            else:
                no_asignados.append(estudiante)

        print(f"Estrategia ejecutada: {self.nombre_segmento}")

        return asignados, no_asignados, cupos_no_usados