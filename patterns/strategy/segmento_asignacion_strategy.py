class SegmentoAsignacionStrategy:
    def __init__(self, nombre_segmento, porcentaje_cupos):
        self.nombre_segmento = nombre_segmento
        self.porcentaje_cupos = porcentaje_cupos

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
