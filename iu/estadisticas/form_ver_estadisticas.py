import tkinter as tk
from tkinter import ttk, messagebox

from iu.base.ventana_base import VentanaBase
from services.estadisticas_service import EstadisticasService


class VerEstadisticasView(VentanaBase):

    def __init__(self, master=None):
        super().__init__(
            master,
            titulo="Estadísticas de Asignación",
            ancho=500,
            alto=450
        )

        self.service = EstadisticasService()
        self._crear_widgets()
        self._cargar_estadisticas()

    def _crear_widgets(self):
        self.contenedor = ttk.Frame(self)
        self.contenedor.pack(expand=True, fill="both", padx=20, pady=20)

        ttk.Label(
            self.contenedor,
            text="Estadísticas Generales",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        self.texto = tk.Text(self.contenedor, height=20)
        self.texto.pack(expand=True, fill="both")
        self.texto.configure(state="disabled")

        ttk.Button(
            self.contenedor,
            text="Cerrar",
            width=20,
            command=self.destroy
        ).pack(pady=10)

    def _cargar_estadisticas(self):
        try:
            est = self.service.obtener_estadisticas()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        self.texto.configure(state="normal")
        self.texto.delete("1.0", tk.END)

        self.texto.insert(tk.END, f"Total de postulantes: {est['total']}\n")
        self.texto.insert(tk.END, f"Asignados: {est['asignados']}\n")
        self.texto.insert(tk.END, f"No asignados: {est['no_asignados']}\n")
        self.texto.insert(
            tk.END,
            f"Porcentaje de asignación: {est['porcentaje']}%\n\n"
        )

        self.texto.insert(tk.END, "Asignados por carrera:\n")
        self.texto.insert(tk.END, "---------------------------\n")

        for carrera, cantidad in est["por_carrera"].items():
            self.texto.insert(tk.END, f"{carrera}: {cantidad}\n")

        self.texto.configure(state="disabled")
