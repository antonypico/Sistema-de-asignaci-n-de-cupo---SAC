import csv
import json
import os

from domain.oferta_academica import OfertaAcademica
from services.periodo_service import PeriodoService


class OfertaAcademicaService:
    ARCHIVO = "data/ofertas_academicas.json"

    def __init__(self):
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(self.ARCHIVO):
            with open(self.ARCHIVO, "w", encoding="utf-8") as f:
                json.dump([], f)

        self.periodo_service = PeriodoService()

   
    # Persistencia
   

    def _leer_ofertas(self):
        try:
            with open(self.ARCHIVO, "r", encoding="utf-8") as f:
                contenido = f.read().strip()
                if not contenido:
                    return []
                data = json.loads(contenido)
                return [OfertaAcademica.desde_diccionario(o) for o in data]
        except:
            return []

    def _guardar_ofertas(self, ofertas):
        with open(self.ARCHIVO, "w", encoding="utf-8") as f:
            json.dump(
                [o.a_diccionario() for o in ofertas],
                f,
                indent=4,
                ensure_ascii=False
            )

   
    # Carga desde CSV
   

    def cargar_desde_csv(self, ruta_csv):
        periodo = self.periodo_service.obtener_periodo_activo()
        if not periodo:
            raise ValueError("No existe un período activo")

        ofertas = self._leer_ofertas()

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

        self._guardar_ofertas(ofertas)
