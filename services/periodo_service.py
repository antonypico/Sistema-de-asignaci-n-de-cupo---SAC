import json
import os
import re

from domain.periodo import Periodo


class PeriodoService:
    ARCHIVO = "data/periodos.json"
    FORMATO_REGEX = r"^\d{4}-[12]$"

    def __init__(self):
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(self.ARCHIVO):
            with open(self.ARCHIVO, "w", encoding="utf-8") as f:
                json.dump([], f)

    # ------------------------
    # Persistencia
    # ------------------------

    def _leer_periodos(self):
        try:
            with open(self.ARCHIVO, "r", encoding="utf-8") as f:
                contenido = f.read().strip()
                if not contenido:
                    return []
                data = json.loads(contenido)
                return [Periodo.desde_diccionario(p) for p in data]
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _guardar_periodos(self, periodos):
        with open(self.ARCHIVO, "w", encoding="utf-8") as f:
            json.dump(
                [p.a_diccionario() for p in periodos],
                f,
                indent=4,
                ensure_ascii=False
            )

    # ------------------------
    # Reglas de negocio
    # ------------------------

    def validar_formato_nombre(self, nombre):
        return re.match(self.FORMATO_REGEX, nombre) is not None

    def listar_periodos(self):
        return self._leer_periodos()

    def obtener_periodo_activo(self):
        for p in self._leer_periodos():
            if p.activo:
                return p
        return None

    def crear_periodo(self, nombre, fecha_inicio, fecha_fin):
        if not self.validar_formato_nombre(nombre):
            raise ValueError("El formato del período debe ser YYYY-1 o YYYY-2")

        periodos = self._leer_periodos()

        if any(p.nombre == nombre for p in periodos):
            raise ValueError("Ya existe un período con ese nombre")

        if any(p.activo for p in periodos):
            raise ValueError("Ya existe un período activo. Debe finalizarlo o eliminarlo")

        nuevo = Periodo(nombre, fecha_inicio, fecha_fin, activo=True)
        periodos.append(nuevo)
        self._guardar_periodos(periodos)

        return nuevo

    def finalizar_periodo_activo(self):
        periodos = self._leer_periodos()

        for p in periodos:
            if p.activo:
                p.finalizar()
                self._guardar_periodos(periodos)
                return p

        raise ValueError("No existe un período activo")

    def eliminar_periodo(self, nombre_periodo):
        periodos = self._leer_periodos()

        periodo = next((p for p in periodos if p.nombre == nombre_periodo), None)

        if not periodo:
            raise ValueError("El período no existe")

        periodos.remove(periodo)
        self._guardar_periodos(periodos)

        return periodo
