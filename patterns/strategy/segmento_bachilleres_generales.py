from patterns.strategy.segmento_asignacion_strategy import SegmentoAsignacionStrategy


class SegmentoBachillerGeneral(SegmentoAsignacionStrategy):

    def __init__(self):
        super().__init__(
            nombre_segmento="Bachilleres Generales",
            porcentaje_cupos=0.25
        )

    def asignar(self, estudiantes, ofertas):
        asignados = []
        no_asignados = []
        cupos_no_usados = 0

        postulantes = [
            e for e in estudiantes
            if not e.tiene_titulo_superior
            and not e.es_pueblo_nacionalidad
            and not e.esta_asignado()
        ]

        postulantes.sort(key=lambda e: e.nota_postulacion, reverse=True)

        for estudiante in postulantes:
            for opcion in estudiante.opciones_carrera:
                oferta = next(
                    (o for o in ofertas if o.codigo_carrera == opcion and o.tiene_cupos()),
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