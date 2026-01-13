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
            ancho=700,
            alto=500
        )

        self._crear_widgets()
        self._cargar_resultados()

    def _crear_widgets(self):
        contenedor = ttk.Frame(self)
        contenedor.pack(expand=True, fill="both", padx=20, pady=20)

        ttk.Label(
            contenedor,
            text="Resultados de la Asignación",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        # Área de texto con scroll
        frame_texto = ttk.Frame(contenedor)
        frame_texto.pack(expand=True, fill="both")

        self.texto = tk.Text(frame_texto, wrap="none")
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
                    f"{r['id_postulante']} | "
                    f"{r['nombre_completo']} | "
                    f"{r['resultado']}\n"
                )
                self.texto.insert(tk.END, linea)

        self.texto.configure(state="disabled")
