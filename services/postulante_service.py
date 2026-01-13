import csv
import json
import os

from domain.estudiante import Estudiante


class PostulanteService:
    ARCHIVO = "data/postulantes.json"

    def __init__(self):
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(self.ARCHIVO):
            with open(self.ARCHIVO, "w", encoding="utf-8") as f:
                json.dump([], f)

    # ------------------
    # Persistencia
    # ------------------

    def _guardar_postulantes(self, postulantes):
        with open(self.ARCHIVO, "w", encoding="utf-8") as f:
            json.dump(
                [p.a_diccionario() for p in postulantes],
                f,
                indent=4,
                ensure_ascii=False
            )

    # ------------------
    # Carga desde CSV
    # ------------------

    def cargar_desde_csv(self, ruta_csv):
        postulantes = []

        with open(ruta_csv, newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)

            columnas_requeridas = [
                "id_postulante",
                "correo",
                "num_telefono",
                "nombres",
                "apellidos",
                "nota_postulacion",
                "opcion_1",
                "politica_cuotas",
                "vulnerable",
                "cuadro_honor",
                "pueblo_nacionalidad",
                "titulo_superior"
            ]

            if not all(col in lector.fieldnames for col in columnas_requeridas):
                raise ValueError("El archivo CSV no tiene el formato correcto")

            for fila in lector:
                estudiante = Estudiante(
                    id_postulante=fila["id_postulante"],
                    correo=fila["correo"],
                    num_telefono=fila["num_telefono"],
                    nombres=fila["nombres"],
                    apellidos=fila["apellidos"],
                    nota_postulacion=fila["nota_postulacion"],
                    opcion_carrera=fila["opcion_1"],
                    es_politica_cuotas=fila["politica_cuotas"] == "SI",
                    es_vulnerable=fila["vulnerable"] == "SI",
                    es_cuadro_honor=fila["cuadro_honor"] == "SI",
                    es_pueblo_nacionalidad=fila["pueblo_nacionalidad"] == "SI",
                    tiene_titulo_superior=fila["titulo_superior"] == "SI"
                )
                postulantes.append(estudiante)

        self._guardar_postulantes(postulantes)
