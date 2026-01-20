from patterns.strategy.segmento_asignacion_strategy import SegmentoAsignacionStrategy


class SegmentoBachillerPN(SegmentoAsignacionStrategy):

    def __init__(self):
        super().__init__(
            nombre_segmento="Bachilleres Pueblos y Nacionalidades",
            porcentaje_cupos=0.05
        )

    def asignar(self, estudiantes, ofertas):
        asignados = []
        no_asignados = []
        cupos_no_usados = 0

        postulantes = [
            e for e in estudiantes
            if e.es_pueblo_nacionalidad and not e.esta_asignado() and not e.perdio_desempate
        ]

        postulantes.sort(key=lambda e: e.nota_postulacion, reverse=True)
        
        # Aplicar desempate a estudiantes con la misma nota
        ganadores, perdedores = self._aplicar_desempate(postulantes)
        
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