import tkinter as tk
from tkinter import ttk, messagebox

from iu.base.ventana_base import VentanaBase
from services.asignacion_service import AsignacionService


class EjecutarAsignacionView(VentanaBase):

    def __init__(self, master=None):
        super().__init__(
            master,
            titulo="Ejecutar Asignación de Cupos",
            ancho=450,
            alto=250
        )

        self.service = AsignacionService()
        self._crear_widgets()

    def _crear_widgets(self):
        contenedor = ttk.Frame(self)
        contenedor.pack(expand=True, padx=20, pady=20)

        ttk.Label(
            contenedor,
            text="Ejecutar asignación de cupos",
            font=("Arial", 14, "bold")
        ).pack(pady=15)

        ttk.Label(
            contenedor,
            text="Este proceso asignará los cupos disponibles\na los postulantes cargados.",
            justify="center"
        ).pack(pady=10)

        ttk.Button(
            contenedor,
            text="Ejecutar asignación",
            width=30,
            command=self._ejecutar
        ).pack(pady=10)

        ttk.Button(
            contenedor,
            text="Cancelar",
            width=20,
            command=self.destroy
        ).pack(pady=5)

    def _ejecutar(self):
        try:
            self.service.ejecutar_asignacion()
            messagebox.showinfo(
                "Éxito",
                "La asignación de cupos se ejecutó correctamente"
            )
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
