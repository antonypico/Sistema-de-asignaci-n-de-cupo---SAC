import json
import os
import csv

from domain.estudiante import Estudiante
from services.periodo_service import PeriodoService


class PostulanteService:

    def __init__(self):
        self.periodo_service = PeriodoService()

    # -------------------------------------------------
    # UTILIDAD: ARCHIVO DEL PERIODO ACTIVO
    # -------------------------------------------------

    def _archivo_postulantes(self):
        ruta = self.periodo_service.obtener_ruta_periodo_activo()
        return f"{ruta}/postulantes.json"

    # -------------------------------------------------
    # LEER POSTULANTES
    # -------------------------------------------------

    def leer_postulantes(self):
        archivo = self._archivo_postulantes()

        if not os.path.exists(archivo):
            return []

        with open(archivo, "r", encoding="utf-8") as f:
            data = json.load(f)

        return [Estudiante.desde_diccionario(p) for p in data]

    # -------------------------------------------------
    # GUARDAR POSTULANTES
    # -------------------------------------------------

    def guardar_postulantes(self, postulantes):
        archivo = self._archivo_postulantes()

        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(
                [p.a_diccionario() for p in postulantes],
                f,
                indent=4,
                ensure_ascii=False
            )

    # -------------------------------------------------
    # CARGAR POSTULANTES DESDE CSV
    # -------------------------------------------------

    def cargar_desde_csv(self, ruta_csv):
        postulantes = []

        with open(ruta_csv, newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)

            for fila in lector:
                estudiante = Estudiante(
                    id_postulante=fila["id_postulante"],
                    correo=fila["correo"],
                    num_telefono=fila["num_telefono"],
                    nombres=fila["nombres"],
                    apellidos=fila["apellidos"],
                    nota_postulacion=fila["nota_postulacion"],
                    opcion_1=fila["opcion_1"],
                    politica_cuotas=bool(int(fila["politica_cuotas"])),
                    vulnerable=bool(int(fila["vulnerable"])),
                    cuadro_honor=bool(int(fila["cuadro_honor"])),
                    pueblo_nacionalidad=bool(int(fila["pueblo_nacionalidad"])),
                    titulo_superior=bool(int(fila["titulo_superior"])),
                    otro_merito=bool(int(fila["otro_merito"]))
                )
                postulantes.append(estudiante)

        self.guardar_postulantes(postulantes)
