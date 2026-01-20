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
            if e.es_vulnerable and not e.esta_asignado() and not e.perdio_desempate
        ]

        vulnerables.sort(key=lambda e: e.nota_postulacion, reverse=True)
        
        # Aplicar desempate a estudiantes con la misma nota
        ganadores, perdedores = self._aplicar_desempate(vulnerables)
        
        # Los perdedores del desempate NO se asignan
        for estudiante in ganadores:
            for opcion in estudiante.opciones_carrera:
                oferta = self._buscar_oferta(opcion, ofertas)
                if oferta:
                    oferta.consumir_cupo()
                    estudiante.marcar_asignado(oferta)
                    asignados.append(estudiante)
                    break
            else:
                no_asignados.append(estudiante)
        
        # Los perdedores del desempate van a no_asignados (sin marcar como asignados)
        no_asignados.extend(perdedores)

        print(f"Estrategia ejecutada: {self.nombre_segmento}")
        return asignados, no_asignados, cupos_no_usados