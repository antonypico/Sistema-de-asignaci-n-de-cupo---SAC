import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

from iu.base.ventana_base import VentanaBase


class VerResultadosView(VentanaBase):

    ARCHIVO = "data/resultados_asignacion.json"

    def __init__(self, master=None):
        super().__init__(
            master,
            titulo="Resultados de la Asignación de Cupos",
            ancho=750,
            alto=550
        )

        self._crear_widgets()
        self._cargar_resultados()

    def _crear_widgets(self):
        contenedor = ttk.Frame(self)
        contenedor.pack(expand=True, fill="both", padx=20, pady=20)

        ttk.Label(
            contenedor,
            text="Resultados de la Asignación de Cupos",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        frame_texto = ttk.Frame(contenedor)
        frame_texto.pack(expand=True, fill="both")

        self.texto = tk.Text(frame_texto, wrap="word")
        self.texto.pack(side="left", expand=True, fill="both")

        scroll = ttk.Scrollbar(frame_texto, orient="vertical", command=self.texto.yview)
        scroll.pack(side="right", fill="y")

        self.texto.configure(yscrollcommand=scroll.set, state="disabled")

        ttk.Button(
            contenedor,
            text="Cerrar",
            width=20,
            command=self.destroy
        ).pack(pady=10)

    def _cargar_resultados(self):
        if not os.path.exists(self.ARCHIVO):
            messagebox.showwarning(
                "Sin resultados",
                "Aún no se ha ejecutado la asignación de cupos"
            )
            return

        with open(self.ARCHIVO, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.texto.configure(state="normal")
        self.texto.delete("1.0", tk.END)

        if not data:
            self.texto.insert(tk.END, "No existen resultados registrados.\n")
        else:
            for r in data:
                linea = (
                    f"ID Estudiante: {r['id_estudiante']}\n"
                    f"Nombres: {r['nombres']} {r['apellidos']}\n"
                    f"Correo: {r['correo']}\n"
                    f"Carrera: {r['carrera']}\n"
                    f"Jornada: {r['jornada']}\n"
                    f"Modalidad: {r['modalidad']}\n"
                    f"Nota de postulación: {r['nota_postulacion']}\n"
                    f"Grupo: {r['grupo']}\n"
                    f"Estado de asignación: {r['estado_asignacion']}\n"
                    f"{'-'*70}\n"
                )
                self.texto.insert(tk.END, linea)

        self.texto.configure(state="disabled")
