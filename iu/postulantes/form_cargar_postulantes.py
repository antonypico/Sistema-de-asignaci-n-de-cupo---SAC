import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from iu.base.ventana_base import VentanaBase
from services.postulante_service import PostulanteService
from services.periodo_service import PeriodoService


class CargarPostulantesView(VentanaBase):

    def __init__(self, master=None):
        super().__init__(
            master,
            titulo="Cargar Ficha de Postulantes",
            ancho=450,
            alto=300
        )

        self.postulante_service = PostulanteService()
        self.periodo_service = PeriodoService()

        self._crear_widgets()

    def _crear_widgets(self):
        contenedor = ttk.Frame(self)
        contenedor.pack(expand=True, padx=20, pady=20)

        periodo = self.periodo_service.obtener_periodo_activo()

        ttk.Label(
            contenedor,
            text="Cargar ficha de postulantes",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        ttk.Label(
            contenedor,
            text=f"Período activo: {periodo.nombre if periodo else 'Ninguno'}"
        ).pack(pady=5)

        ttk.Button(
            contenedor,
            text="Seleccionar archivo CSV",
            width=30,
            command=self._cargar_csv
        ).pack(pady=15)

        ttk.Button(
            contenedor,
            text="Cerrar",
            width=20,
            command=self.destroy
        ).pack(pady=5)

    def _cargar_csv(self):
        ruta = filedialog.askopenfilename(
            filetypes=[("Archivos CSV", "*.csv")]
        )

        if not ruta:
            return

        try:
            self.postulante_service.cargar_desde_csv(ruta)
            messagebox.showinfo(
                "Éxito",
                "Postulantes cargados correctamente"
            )
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
