import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from iu.base.ventana_base import VentanaBase
from services.oferta_academica_service import OfertaAcademicaService
from services.periodo_service import PeriodoService


class ConfigurarCarreraView(VentanaBase):
    def __init__(self, master=None):
        super().__init__(
            master,
            titulo="Configurar Oferta Académica",
            ancho=600,
            alto=350
        )

        self.oferta_service = OfertaAcademicaService()
        self.periodo_service = PeriodoService()

        self._crear_widgets()

    def _crear_widgets(self):
        contenedor = ttk.Frame(self)
        contenedor.pack(expand=True, fill="both", padx=20, pady=20)

        periodo = self.periodo_service.obtener_periodo_activo()
        nombre_periodo = periodo.nombre if periodo else "NO ACTIVO"

        ttk.Label(
            contenedor,
            text="Configuración de Oferta Académica",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        ttk.Label(
            contenedor,
            text=f"Período activo: {nombre_periodo}",
            font=("Arial", 11)
        ).pack(pady=5)

        ttk.Separator(contenedor).pack(fill="x", pady=15)

        ttk.Label(
            contenedor,
            text="Cargar archivo CSV de oferta académica",
            font=("Arial", 11, "bold")
        ).pack(pady=10)

        ttk.Button(
            contenedor,
            text="Seleccionar archivo CSV",
            width=35,
            command=self._seleccionar_archivo
        ).pack(pady=10)

        ttk.Button(
            contenedor,
            text="Cerrar",
            command=self.destroy
        ).pack(pady=15)

    def _seleccionar_archivo(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo CSV",
            filetypes=[("Archivos CSV", "*.csv")]
        )

        if not ruta:
            return

        try:
            self.oferta_service.cargar_desde_csv(ruta)

            messagebox.showinfo(
                "Éxito",
                "La oferta académica fue cargada correctamente"
            )

        except ValueError as e:
            messagebox.showwarning("Advertencia", str(e))

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Ocurrió un error al cargar el archivo:\n{e}"
            )
