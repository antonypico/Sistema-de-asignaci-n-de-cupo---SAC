from patterns.strategy.segmento_asignacion_strategy import SegmentoAsignacionStrategy


class SegmentoMeritoAcademico(SegmentoAsignacionStrategy):

    def __init__(self):
        super().__init__(
            nombre_segmento="Mérito Académico",
            porcentaje_cupos=0.20
        )

    def asignar(self, estudiantes, ofertas):
        asignados = []
        no_asignados = []
        cupos_no_usados = 0

        merito = [
            e for e in estudiantes
            if e.es_cuadro_honor and not e.esta_asignado()
        ]

        merito.sort(key=lambda e: e.nota_postulacion, reverse=True)

        for estudiante in merito:
            for opcion in estudiante.opciones_carrera:
                oferta = self._buscar_oferta(opcion, ofertas)
                if oferta:
                    oferta.consumir_cupo()
                    estudiante.marcar_asignado(oferta)
                    asignados.append(estudiante)
                    break
            else:
                no_asignados.append(estudiante)

        print(f"Estrategia ejecutada: {self.nombre_segmento}")
        return asignados, no_asignados, cupos_no_usados