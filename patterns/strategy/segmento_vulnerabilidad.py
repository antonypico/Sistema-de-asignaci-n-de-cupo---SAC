from patterns.strategy.segmento_asignacion_strategy import SegmentoAsignacionStrategy


class SegmentoVulnerabilidad(SegmentoAsignacionStrategy):

    def __init__(self):
        super().__init__(
            nombre_segmento="Vulnerabilidad Socioeconómica",
            porcentaje_cupos=0.20
        )

    def asignar(self, estudiantes, ofertas):
        asignados = []
        no_asignados = []
        cupos_no_usados = 0

        vulnerables = [
            e for e in estudiantes
            if e.es_vulnerable and not e.esta_asignado()
        ]

        vulnerables.sort(key=lambda e: e.nota_postulacion, reverse=True)

        for estudiante in vulnerables:
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

        for e in estudiantes:
            if e not in vulnerables:
                no_asignados.append(e)

        print(f"Estrategia ejecutada: {self.nombre_segmento}")

        return asignados, no_asignados, cupos_no_usados


