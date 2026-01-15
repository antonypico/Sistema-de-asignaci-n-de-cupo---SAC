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
        estudiantes = self._leer_postulantes()
        ofertas = self._leer_ofertas()

        if not estudiantes:
            raise ValueError("No existen estudiantes cargados")

        if not ofertas:
            raise ValueError("No existe oferta académica cargada")

        asignador = AsignadorCupos(estudiantes, ofertas)
        resultados = asignador.ejecutar()

        self._guardar_resultados(resultados)

    # -------------------------
    # LECTURA DE DATOS
    # -------------------------

    def _leer_postulantes(self):
        with open("data/postulantes.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Estudiante.desde_diccionario(e) for e in data]

    def _leer_ofertas(self):
        return self.oferta_service._leer_ofertas()

    # -------------------------
    # GUARDAR RESULTADOS
    # -------------------------

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

                "carrera": oferta.carrera.nombre if oferta else None,
                "jornada": oferta.jornada if oferta else None,
                "modalidad": oferta.modalidad if oferta else None,

                "grupo": self._determinar_grupo(estudiante),
                "estado_asignacion": "ASIGNADO" if estudiante.esta_asignado() else "NO ASIGNADO"
            })

        with open(self.ARCHIVO_RESULTADOS, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    # -------------------------
    # DETERMINAR GRUPO
    # -------------------------

    def _determinar_grupo(self, estudiante):
        if estudiante.es_politica_cuotas:
            return "Política de Cuotas"
        if estudiante.es_vulnerable:
            return "Vulnerabilidad"
        if estudiante.es_cuadro_honor:
            return "Mérito Académico"
        if estudiante.es_pueblo_nacionalidad:
            return "Bachiller Pueblos y Nacionalidades"
        if estudiante.tiene_otro_merito:
            return "Otros Méritos"
        return "Población General"
