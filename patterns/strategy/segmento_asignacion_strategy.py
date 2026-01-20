from itertools import groupby


class SegmentoAsignacionStrategy:
    def __init__(self, nombre_segmento, porcentaje_cupos):
        self.nombre_segmento = nombre_segmento
        self.porcentaje_cupos = porcentaje_cupos
        self.desempate_service = None  # Se inyectará desde fuera

    def _buscar_oferta(self, opcion, ofertas):
        """
        Busca una oferta académica por:
        - código de carrera (IS1)
        - nombre de carrera (Ingeniería en Sistemas)
        """
        opcion_normalizada = opcion.strip().lower()

        for oferta in ofertas:
            if (
                opcion_normalizada == oferta.codigo_carrera.strip().lower()
                or opcion_normalizada == oferta.nombre_carrera.strip().lower()
            ) and oferta.tiene_cupos():
                return oferta

        return None

    def _aplicar_desempate(self, estudiantes):
        """
        Aplica desempate a estudiantes con igual nota
        
        Args:
            estudiantes: Lista de estudiantes ya ordenados por nota (descendente)
            
        Returns:
            Tupla: (ganadores_desempate, perdedores_desempate)
            - ganadores: estudiantes que ganaron el desempate (1 por grupo)
            - perdedores: estudiantes que perdieron el desempate
        """
        if not self.desempate_service:
            # Si no hay servicio de desempate, todos son "ganadores"
            return estudiantes, []
        
        ganadores = []
        perdedores = []
        
        # Agrupar por nota
        estudiantes_ordenados = sorted(estudiantes, key=lambda e: e.nota_postulacion, reverse=True)
        
        for nota, grupo in groupby(estudiantes_ordenados, key=lambda e: e.nota_postulacion):
            grupo_list = list(grupo)
            
            if len(grupo_list) > 1:
                # Aplicar desempate si hay más de uno con la misma nota
                grupo_desempatado = self.desempate_service.aplicar_desempate(
                    self.nombre_segmento,
                    grupo_list
                )
                
                # El primero es el ganador, los demás pierden el desempate
                ganador = grupo_desempatado[0]
                ganador.observaciones = f"Se asignó el cupo al ganar el desempate en {self.nombre_segmento}"
                ganadores.append(ganador)
                
                for idx, estudiante in enumerate(grupo_desempatado[1:], 1):
                    estudiante.observaciones = f"No se asignó cupo porque perdió el desempate en {self.nombre_segmento}"
                    estudiante.perdio_desempate = True  # Marca como perdedor del desempate
                    perdedores.append(estudiante)
            else:
                ganadores.extend(grupo_list)
        
        return ganadores, perdedores
    
    def establecer_desempate_service(self, desempate_service):
        """Inyecta el servicio de desempate"""
        self.desempate_service = desempate_service