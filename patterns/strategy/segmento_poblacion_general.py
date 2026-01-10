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
        cupos_no_usados = 0  # aquí ya no se usa, pero mantenemos el contrato

        # Todos los estudiantes que aún no han sido asignados
        postulantes = [
            e for e in estudiantes
            if not e.esta_asignado()
        ]

        # Meritocracia: mayor nota primero
        postulantes.sort(key=lambda e: e.nota_postulacion, reverse=True)

        for estudiante in postulantes:
            asignado = False
            for opcion in estudiante.opciones_carrera:
                oferta = next(
                    (o for o in ofertas if o.carrera.nombre == opcion),
                    None
                )

                if oferta and oferta.tiene_cupos():
                    oferta.consumir_cupo()
                    estudiante.marcar_asignado(oferta)
                    asignados.append(estudiante)
                    asignado = True
                    break

            if not asignado:
                no_asignados.append(estudiante)

        print(f"Estrategia ejecutada: {self.nombre_segmento}")

        return asignados, no_asignados, cupos_no_usados

