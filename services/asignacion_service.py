import json
import os

from domain.estudiante import Estudiante
from services.postulante_service import PostulanteService
from services.oferta_academica_service import OfertaAcademicaService
from services.asignador_cupos import AsignadorCupos


class AsignacionService:

    ARCHIVO_RESULTADOS = "data/resultados_asignacion.json"

    def __init__(self):
        os.makedirs("data", exist_ok=True)
        self.postulante_service = PostulanteService()
        self.oferta_service = OfertaAcademicaService()

    # -------------------------
    # PROCESO PRINCIPAL
    # -------------------------

    def ejecutar_asignacion(self):
        postulantes = self._leer_postulantes()
        ofertas = self._leer_ofertas()

        if not postulantes:
            raise ValueError("No existen postulantes cargados")

        if not ofertas:
            raise ValueError("No existe oferta académica cargada")

        asignador = AsignadorCupos(postulantes, ofertas)
        resultados = asignador.ejecutar()

        self._guardar_resultados(resultados)

    # -------------------------
    # LECTURA DE DATOS
    # -------------------------

    def _leer_postulantes(self):
        """
        Convierte el JSON en objetos Estudiante
        """
        with open("data/postulantes.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Estudiante.desde_diccionario(p) for p in data]

    def _leer_ofertas(self):
        """
        Las ofertas ya se usan como objetos en memoria
        """
        return self.oferta_service._leer_ofertas()

    # -------------------------
    # GUARDAR RESULTADOS
    # -------------------------

    def _guardar_resultados(self, resultados):
        data = []

        for r in resultados:
            data.append({
                "id_postulante": r.estudiante.id_postulante,
                "nombre_completo": r.estudiante.nombre_completo(),
                "resultado": r.resultado
            })

        with open(self.ARCHIVO_RESULTADOS, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
