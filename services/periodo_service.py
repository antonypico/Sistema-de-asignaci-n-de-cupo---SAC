import json
import os
from datetime import date


class Periodo:
    def __init__(self, nombre, fecha_inicio=None, fecha_fin=None, activo=False):
        self.nombre = nombre
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.activo = activo

    # -----------------------------
    # SERIALIZACIÓN CORRECTA
    # -----------------------------

    def a_diccionario(self):
        return {
            "nombre": self.nombre,
            "fecha_inicio": self.fecha_inicio.isoformat() if self.fecha_inicio else None,
            "fecha_fin": self.fecha_fin.isoformat() if self.fecha_fin else None,
            "activo": self.activo
        }

    @staticmethod
    def desde_diccionario(data):
        return Periodo(
            nombre=data["nombre"],
            fecha_inicio=date.fromisoformat(data["fecha_inicio"])
            if data.get("fecha_inicio") else None,
            fecha_fin=date.fromisoformat(data["fecha_fin"])
            if data.get("fecha_fin") else None,
            activo=data.get("activo", False)
        )


class PeriodoService:

    ARCHIVO = "data/periodos.json"

    def __init__(self):
        os.makedirs("data", exist_ok=True)
        os.makedirs("data/periodos", exist_ok=True)

        if not os.path.exists(self.ARCHIVO):
            with open(self.ARCHIVO, "w", encoding="utf-8") as f:
                json.dump([], f)

    # -------------------------------------------------
    # UTILIDAD CLAVE: RUTA DEL PERIODO ACTIVO
    # -------------------------------------------------

    def obtener_ruta_periodo_activo(self):
        periodo = self.obtener_periodo_activo()
        if not periodo:
            raise ValueError("No existe un período activo")

        ruta = f"data/periodos/{periodo.nombre}"
        os.makedirs(ruta, exist_ok=True)
        return ruta

    # -------------------------------------------------
    # CRUD DE PERIODOS
    # -------------------------------------------------

    def crear_periodo(self, nombre, fecha_inicio=None, fecha_fin=None):
        periodos = self._leer_periodos()

        # Desactivar todos
        for p in periodos:
            p.activo = False

        nuevo = Periodo(
            nombre=nombre,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            activo=True
        )

        periodos.append(nuevo)
        self._guardar_periodos(periodos)

        # Crear carpeta del período
        os.makedirs(f"data/periodos/{nombre}", exist_ok=True)

    def listar_periodos(self):
        return self._leer_periodos()

    def obtener_periodo_activo(self):
        periodos = self._leer_periodos()
        for p in periodos:
            if p.activo:
                return p
        return None

    def activar_periodo(self, nombre):
        periodos = self._leer_periodos()
        encontrado = False

        for p in periodos:
            if p.nombre == nombre:
                p.activo = True
                encontrado = True
            else:
                p.activo = False

        if not encontrado:
            raise ValueError("Período no encontrado")

        self._guardar_periodos(periodos)
        os.makedirs(f"data/periodos/{nombre}", exist_ok=True)

    # -------------------------------------------------
    # PERSISTENCIA
    # -------------------------------------------------

    def _leer_periodos(self):
        with open(self.ARCHIVO, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Periodo.desde_diccionario(p) for p in data]

    def _guardar_periodos(self, periodos):
        with open(self.ARCHIVO, "w", encoding="utf-8") as f:
            json.dump(
                [p.a_diccionario() for p in periodos],
                f,
                indent=4,
                ensure_ascii=False
            )


    # -------------------------------------------------
    # FINALIZAR PERIODO ACTIVO
    # -------------------------------------------------

    def finalizar_periodo_activo(self):
        periodos = self._leer_periodos()
        periodo_finalizado = None

        for p in periodos:
            if p.activo:
                p.activo = False
                periodo_finalizado = p
                break

        if not periodo_finalizado:
            raise ValueError("No existe un período activo para finalizar")

        self._guardar_periodos(periodos)
        return periodo_finalizado


    # -------------------------------------------------
    # ELIMINAR PERIODO
    # -------------------------------------------------

    def eliminar_periodo(self, nombre):
        periodos = self._leer_periodos()
        periodo_a_eliminar = None

        for p in periodos:
            if p.nombre == nombre:
                periodo_a_eliminar = p
                break

        if not periodo_a_eliminar:
            raise ValueError("El período no existe")

        if periodo_a_eliminar.activo:
            raise ValueError("No se puede eliminar un período activo")

        # Eliminar del listado
        periodos = [p for p in periodos if p.nombre != nombre]
        self._guardar_periodos(periodos)

        # Eliminar carpeta del período (si existe)
        ruta = f"data/periodos/{nombre}"
        if os.path.exists(ruta):
            for archivo in os.listdir(ruta):
                os.remove(os.path.join(ruta, archivo))
            os.rmdir(ruta)
