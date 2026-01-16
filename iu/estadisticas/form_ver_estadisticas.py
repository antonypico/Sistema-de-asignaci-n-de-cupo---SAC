import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from collections import defaultdict

from iu.base.ventana_base import VentanaBase
from services.periodo_service import PeriodoService


class VerEstadisticasView(VentanaBase):

    def __init__(self, master=None):
        super().__init__(
            master,
            titulo="Estadísticas de Asignación",
            ancho=800,
            alto=600
        )

        self.periodo_service = PeriodoService()

        self._crear_widgets()
        self._cargar_estadisticas()

    def _crear_widgets(self):
        contenedor = ttk.Frame(self)
        contenedor.pack(expand=True, fill="both", padx=20, pady=20)

        ttk.Label(
            contenedor,
            text="Estadísticas de Asignación de Cupos",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        self.texto = tk.Text(contenedor, wrap="word")
        self.texto.pack(expand=True, fill="both")
        self.texto.configure(state="disabled")

        ttk.Button(
            contenedor,
            text="Cerrar",
            width=20,
            command=self.destroy
        ).pack(pady=10)

    def _cargar_estadisticas(self):
        try:
            ruta = self.periodo_service.obtener_ruta_periodo_activo()

            archivo_resultados = f"{ruta}/resultados_asignacion.json"
            archivo_ofertas = f"{ruta}/ofertas_academicas.json"

            if not os.path.exists(archivo_resultados):
                raise FileNotFoundError

            if not os.path.exists(archivo_ofertas):
                raise FileNotFoundError

            with open(archivo_resultados, "r", encoding="utf-8") as f:
                resultados = json.load(f)

            with open(archivo_ofertas, "r", encoding="utf-8") as f:
                ofertas = json.load(f)

            # ==================================================
            # 1️⃣ ESTADÍSTICAS GENERALES
            # ==================================================

            total_postulantes = len(resultados)
            total_asignados = sum(
                1 for r in resultados if r["estado_asignacion"] == "ASIGNADO"
            )
            total_no_asignados = total_postulantes - total_asignados

            porcentaje_global = (
                (total_asignados / total_postulantes) * 100
                if total_postulantes > 0 else 0
            )

            # ==================================================
            # 2️⃣ ESTADÍSTICAS POR CARRERA
            # ==================================================

            cupos_por_carrera = {}
            for o in ofertas:
                cupos_por_carrera[o["nombre_carrera"]] = {
                    "total": o["total_cupos"],
                    "disponibles": o["cupos_disponibles"]
                }

            asignados_por_carrera = defaultdict(int)
            for r in resultados:
                if r["estado_asignacion"] == "ASIGNADO" and r["carrera"]:
                    asignados_por_carrera[r["carrera"]] += 1

            # ==================================================
            # MOSTRAR EN PANTALLA
            # ==================================================

            self.texto.configure(state="normal")
            self.texto.delete("1.0", tk.END)

            # ---------- GENERALES ----------
            self.texto.insert(tk.END, "ESTADÍSTICAS GENERALES\n")
            self.texto.insert(tk.END, "-" * 40 + "\n")
            self.texto.insert(tk.END, f"Total de postulantes: {total_postulantes}\n")
            self.texto.insert(tk.END, f"Asignados: {total_asignados}\n")
            self.texto.insert(tk.END, f"No asignados: {total_no_asignados}\n")
            self.texto.insert(
                tk.END,
                f"Porcentaje global de asignación: {porcentaje_global:.2f}%\n\n"
            )

            # ---------- POR CARRERA ----------
            self.texto.insert(tk.END, "ESTADÍSTICAS POR CARRERA\n")
            self.texto.insert(tk.END, "-" * 40 + "\n")

            for carrera, info in cupos_por_carrera.items():
                total = info["total"]
                disponibles = info["disponibles"]
                asignados = asignados_por_carrera.get(carrera, 0)
                porcentaje = (asignados / total) * 100 if total > 0 else 0

                self.texto.insert(tk.END, f"{carrera}\n")
                self.texto.insert(tk.END, f"  Cupos totales: {total}\n")
                self.texto.insert(tk.END, f"  Cupos asignados: {asignados}\n")
                self.texto.insert(tk.END, f"  Cupos disponibles: {disponibles}\n")
                self.texto.insert(tk.END, f"  Ocupación: {porcentaje:.2f}%\n")
                self.texto.insert(tk.END, "-" * 40 + "\n")

            self.texto.configure(state="disabled")

        except Exception:
            messagebox.showerror(
                "Error",
                "No existen resultados de asignación.\n"
                "Ejecute primero la asignación de cupos."
            )
