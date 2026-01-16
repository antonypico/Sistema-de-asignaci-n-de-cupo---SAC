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

    # -------------------------------------------------
    # PROCESO PRINCIPAL DE ASIGNACIÓN
    # -------------------------------------------------

    def ejecutar_asignacion(self):
        estudiantes = self._leer_postulantes()
        ofertas = self._leer_ofertas()

        if not estudiantes:
            raise ValueError("No existen postulantes cargados")

        if not ofertas:
            raise ValueError("No existe oferta académica cargada")

        # Ejecutar asignación
        asignador = AsignadorCupos(estudiantes, ofertas)
        resultados = asignador.ejecutar()

        # Guardar resultados de asignación
        self._guardar_resultados(resultados)

        # 🔥 CLAVE: guardar ofertas con cupos ya consumidos
        self.oferta_service.guardar_ofertas(ofertas)

    # -------------------------------------------------
    # LECTURA DE POSTULANTES
    # -------------------------------------------------

    def _leer_postulantes(self):
        with open("data/postulantes.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Estudiante.desde_diccionario(p) for p in data]

    # -------------------------------------------------
    # LECTURA DE OFERTA ACADÉMICA
    # -------------------------------------------------

    def _leer_ofertas(self):
        return self.oferta_service.leer_ofertas()

    # -------------------------------------------------
    # GUARDAR RESULTADOS
    # -------------------------------------------------

    def _guardar_resultados(self, resultados):
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
                "estado_asignacion": "ASIGNADO" if estudiante.esta_asignado() else "NO ASIGNADO"
            })

        with open(self.ARCHIVO_RESULTADOS, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
