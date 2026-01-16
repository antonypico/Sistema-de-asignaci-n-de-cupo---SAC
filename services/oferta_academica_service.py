import csv
import json
import os

from domain.oferta_academica import OfertaAcademica
from services.periodo_service import PeriodoService


class OfertaAcademicaService:

    def __init__(self):
        self.periodo_service = PeriodoService()

    # -------------------------------------------------
    # UTILIDAD: ARCHIVO DEL PERIODO ACTIVO
    # -------------------------------------------------

    def _archivo_ofertas(self):
        ruta = self.periodo_service.obtener_ruta_periodo_activo()
        return f"{ruta}/ofertas_academicas.json"

    # -------------------------------------------------
    # LEER OFERTAS
    # -------------------------------------------------

    def leer_ofertas(self):
        archivo = self._archivo_ofertas()

        if not os.path.exists(archivo):
            return []

        with open(archivo, "r", encoding="utf-8") as f:
            data = json.load(f)

        return [OfertaAcademica.desde_diccionario(o) for o in data]

    # -------------------------------------------------
    # GUARDAR OFERTAS
    # -------------------------------------------------

    def guardar_ofertas(self, ofertas):
        archivo = self._archivo_ofertas()

        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(
                [o.a_diccionario() for o in ofertas],
                f,
                indent=4,
                ensure_ascii=False
            )

    # -------------------------------------------------
    # CARGAR DESDE CSV (PERIODO ACTIVO)
    # -------------------------------------------------

    def cargar_desde_csv(self, ruta_csv):
        periodo = self.periodo_service.obtener_periodo_activo()
        if not periodo:
            raise ValueError("No existe un período activo")

        ofertas = []

        with open(ruta_csv, newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)

            for fila in lector:
                oferta = OfertaAcademica(
                    codigo_carrera=fila["codigo_carrera"],
                    institucion=fila["institucion"],
                    provincia=fila["provincia"],
                    canton=fila["canton"],
                    nombre_carrera=fila["nombre_carrera"],
                    area=fila["area"],
                    nivel=fila["nivel"],
                    modalidad=fila["modalidad"],
                    jornada=fila["jornada"],
                    tipo_cupo=fila["tipo_cupo"],
                    total_cupos=int(fila["total_cupos"]),
                    periodo=periodo.nombre
                )
                ofertas.append(oferta)

        self.guardar_ofertas(ofertas)

        
