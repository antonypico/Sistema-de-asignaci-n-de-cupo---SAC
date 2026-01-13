import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from iu.base.ventana_base import VentanaBase
from services.postulante_service import PostulanteService


class CargarPostulantesView(VentanaBase):

    def __init__(self, master=None):
        super().__init__(
            master,
            titulo="Cargar ficha de postulantes",
            ancho=500,
            alto=300
        )

        self.service = PostulanteService()
        self._crear_widgets()

    def _crear_widgets(self):
        contenedor = ttk.Frame(self)
        contenedor.pack(expand=True, padx=20, pady=20)

        ttk.Label(
            contenedor,
            text="Cargar ficha de postulantes (CSV)",
            font=("Arial", 14, "bold")
        ).pack(pady=15)

        ttk.Button(
            contenedor,
            text="Seleccionar archivo CSV",
            width=30,
            command=self._cargar_archivo
        ).pack(pady=15)

        ttk.Button(
            contenedor,
            text="Cerrar",
            width=20,
            command=self.destroy
        ).pack(pady=10)

    def _cargar_archivo(self):
        ruta = filedialog.askopenfilename(
            filetypes=[("Archivos CSV", "*.csv")]
        )

        if not ruta:
            return

        try:
            self.service.cargar_desde_csv(ruta)
            messagebox.showinfo(
                "Éxito",
                "La ficha de postulantes se cargó correctamente"
            )
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
