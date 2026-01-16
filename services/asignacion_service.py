import json
import os

from services.postulante_service import PostulanteService
from services.oferta_academica_service import OfertaAcademicaService
from services.periodo_service import PeriodoService
from services.asignador_cupos import AsignadorCupos


class AsignacionService:

    def __init__(self):
        self.periodo_service = PeriodoService()
        self.postulante_service = PostulanteService()
        self.oferta_service = OfertaAcademicaService()

    # -------------------------------------------------
    # PROCESO PRINCIPAL
    # -------------------------------------------------

    def ejecutar_asignacion(self):
        # 👇 SOLO se leen postulantes desde el service
        postulantes = self.postulante_service.leer_postulantes()
        ofertas = self.oferta_service.leer_ofertas()

        if not postulantes:
            raise ValueError("No existen postulantes cargados para el período activo")

        if not ofertas:
            raise ValueError("No existe oferta académica cargada para el período activo")

        asignador = AsignadorCupos(postulantes, ofertas)
        resultados = asignador.ejecutar()

        # Guardar cupos actualizados
        self.oferta_service.guardar_ofertas(ofertas)

        # Guardar resultados
        self._guardar_resultados(resultados)

    # -------------------------------------------------
    # GUARDAR RESULTADOS (PERIODO ACTIVO)
    # -------------------------------------------------

    def _guardar_resultados(self, resultados):
        ruta = self.periodo_service.obtener_ruta_periodo_activo()
        archivo = f"{ruta}/resultados_asignacion.json"

        data = []

        for r in resultados:
            estudiante = r.estudiante
            oferta = estudiante.oferta_asignada

            data.append({
                "id_estudiante": estudiante.id_postulante,
                "nombres": estudiante.nombres,
                "apellidos": estudiante.apellidos,
                "correo": estudiante.correo,
                "nota_postulacion": estudiante.nota_postulacion,
                "carrera": oferta.nombre_carrera if oferta else None,
                "jornada": oferta.jornada if oferta else None,
                "modalidad": oferta.modalidad if oferta else None,
                "estado_asignacion": "ASIGNADO" if oferta else "NO ASIGNADO"
            })

        os.makedirs(ruta, exist_ok=True)

        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


