import json
import os

from domain.oferta_academica import OfertaAcademica


class OfertaAcademicaService:

    ARCHIVO = "data/ofertas_academicas.json"

    def __init__(self):
        os.makedirs("data", exist_ok=True)

    # -------------------------
    # LEER OFERTAS
    # -------------------------

    def _leer_ofertas(self):
        if not os.path.exists(self.ARCHIVO):
            return []

        with open(self.ARCHIVO, "r", encoding="utf-8") as f:
            data = json.load(f)

        return [OfertaAcademica.desde_diccionario(o) for o in data]

    # -------------------------
    # GUARDAR OFERTAS ACTUALIZADAS
    # -------------------------

    def guardar_ofertas(self, ofertas):
        data = [o.a_diccionario() for o in ofertas]

        with open(self.ARCHIVO, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
