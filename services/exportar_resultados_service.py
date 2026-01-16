import json
import csv
import os


class ExportarResultadosService:

    ARCHIVO_JSON = "data/resultados_asignacion.json"

    def exportar_csv(self, ruta_csv):
        if not os.path.exists(self.ARCHIVO_JSON):
            raise ValueError("No existen resultados para exportar")

        with open(self.ARCHIVO_JSON, "r", encoding="utf-8") as f:
            resultados = json.load(f)

        if not resultados:
            raise ValueError("No existen resultados para exportar")

        with open(ruta_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            # Encabezados
            writer.writerow([
                "ID Estudiante",
                "Nombres",
                "Apellidos",
                "Correo",
                "Nota Postulación",
                "Carrera",
                "Jornada",
                "Modalidad",
                "Estado Asignación"
            ])

            # Datos
            for r in resultados:
                writer.writerow([
                    r["id_estudiante"],
                    r["nombres"],
                    r["apellidos"],
                    r["correo"],
                    r["nota_postulacion"],
                    r["carrera"],
                    r["jornada"],
                    r["modalidad"],
                    r["estado_asignacion"]
                ])
