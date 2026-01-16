import tkinter as tk
from tkinter import ttk

from iu.base.ventana_base import VentanaBase
from iu.periodos.form_crear_periodo import CrearPeriodoView
from iu.periodos.form_listar_periodos import ListarPeriodosView
from iu.carreras.form_configurar_carrera import ConfigurarCarreraView
from iu.ofertas.form_ver_ofertas import VerOfertaAcademicaView
from iu.postulantes.form_cargar_postulantes import CargarPostulantesView
from iu.resultados.form_ejecutar_asignacion import EjecutarAsignacionView
from iu.resultados.form_ver_resultados import VerResultadosView
from iu.resultados.form_exportar_resultados import ExportarResultadosView


class MenuPrincipalView(VentanaBase):

    def __init__(self, master=None):
        super().__init__(
            master,
            titulo="Menú Principal - SAC",
            ancho=500,
            alto=520
        )

        self._crear_widgets()

    def _crear_widgets(self):
        contenedor = ttk.Frame(self)
        contenedor.pack(expand=True, padx=20, pady=20)

        ttk.Label(
            contenedor,
            text="Menú Principal",
            font=("Arial", 18, "bold")
        ).pack(pady=20)

        ttk.Button(
            contenedor,
            text="Crear nuevo período",
            width=35,
            command=lambda: CrearPeriodoView(self)
        ).pack(pady=6)

        ttk.Button(
            contenedor,
            text="Listar períodos",
            width=35,
            command=lambda: ListarPeriodosView(self)
        ).pack(pady=6)

        ttk.Button(
            contenedor,
            text="Configurar carreras",
            width=35,
            command=lambda: ConfigurarCarreraView(self)
        ).pack(pady=6)

        ttk.Button(
            contenedor,
            text="Ver oferta académica",
            width=35,
            command=lambda: VerOfertaAcademicaView(self)
        ).pack(pady=6)

        ttk.Button(
            contenedor,
            text="Cargar ficha de postulantes",
            width=35,
            command=lambda: CargarPostulantesView(self)
        ).pack(pady=6)

        ttk.Button(
            contenedor,
            text="Ejecutar asignación de cupos",
            width=35,
            command=lambda: EjecutarAsignacionView(self)
        ).pack(pady=6)

        ttk.Button(
            contenedor,
            text="Ver resultados",
            width=35,
            command=lambda: VerResultadosView(self)
        ).pack(pady=6)

        ttk.Button(
            contenedor,
            text="Exportar resultados",
            width=35,
            command=lambda: ExportarResultadosView(self)
        ).pack(pady=6)

        ttk.Button(
            contenedor,
            text="Salir",
            width=35,
            command=self.destroy
        ).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    MenuPrincipalView(root)
    root.mainloop()
