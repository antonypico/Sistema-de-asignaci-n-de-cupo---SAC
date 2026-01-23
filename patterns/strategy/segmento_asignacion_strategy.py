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
            Lista de estudiantes con desempate aplicado
        """
        if not self.desempate_service:
            return estudiantes
        
        resultado = []
        
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
                resultado.extend(grupo_desempatado)
            else:
                resultado.extend(grupo_list)
        
        return resultado
    
    def establecer_desempate_service(self, desempate_service):
        """Inyecta el servicio de desempate"""
        self.desempate_service = desempate_service