import json
import os
from collections import Counter


class EstadisticasService:

    ARCHIVO = "data/resultados_asignacion.json"

    def obtener_estadisticas(self):
        if not os.path.exists(self.ARCHIVO):
            raise ValueError("No existen resultados de asignación")

        with open(self.ARCHIVO, "r", encoding="utf-8") as f:
            resultados = json.load(f)

        total = len(resultados)
        asignados = [r for r in resultados if r["estado_asignacion"] == "ASIGNADO"]
        no_asignados = total - len(asignados)

        porcentaje = (len(asignados) / total * 100) if total > 0 else 0

        # Conteo por carrera
        carreras = Counter(
            r["carrera"] for r in asignados if r["carrera"] is not None
        )

        return {
            "total": total,
            "asignados": len(asignados),
            "no_asignados": no_asignados,
            "porcentaje": round(porcentaje, 2),
            "por_carrera": carreras
        }
