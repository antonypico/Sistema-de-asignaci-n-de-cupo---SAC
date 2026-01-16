import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from iu.base.ventana_base import VentanaBase
from services.exportar_resultados_service import ExportarResultadosService


class ExportarResultadosView(VentanaBase):

    def __init__(self, master=None):
        super().__init__(
            master,
            titulo="Exportar Resultados",
            ancho=400,
            alto=220
        )

        self.service = ExportarResultadosService()
        self._crear_widgets()

    def _crear_widgets(self):
        contenedor = ttk.Frame(self)
        contenedor.pack(expand=True, padx=20, pady=20)

        ttk.Label(
            contenedor,
            text="Exportar resultados de asignación",
            font=("Arial", 12, "bold")
        ).pack(pady=10)

        ttk.Button(
            contenedor,
            text="Exportar a CSV",
            width=30,
            command=self._exportar
        ).pack(pady=15)

        ttk.Button(
            contenedor,
            text="Cerrar",
            width=20,
            command=self.destroy
        ).pack()

    def _exportar(self):
        ruta = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Archivos CSV", "*.csv")]
        )

        if not ruta:
            return

        try:
            self.service.exportar_csv(ruta)
            messagebox.showinfo(
                "Éxito",
                "Resultados exportados correctamente"
            )
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
