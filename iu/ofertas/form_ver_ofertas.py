import tkinter as tk
from tkinter import ttk, messagebox

from iu.base.ventana_base import VentanaBase
from services.oferta_academica_service import OfertaAcademicaService
from services.periodo_service import PeriodoService


class VerOfertaAcademicaView(VentanaBase):

    def __init__(self, master=None):
        super().__init__(
            master,
            titulo="Oferta Académica",
            ancho=700,
            alto=500
        )

        self.oferta_service = OfertaAcademicaService()
        self.periodo_service = PeriodoService()

        self._crear_widgets()
        self._cargar_ofertas()

    def _crear_widgets(self):
        contenedor = ttk.Frame(self)
        contenedor.pack(expand=True, fill="both", padx=20, pady=20)

        periodo = self.periodo_service.obtener_periodo_activo()
        nombre_periodo = periodo.nombre if periodo else "No definido"

        ttk.Label(
            contenedor,
            text=f"Oferta Académica - Período {nombre_periodo}",
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
            command=self.destroy,
            width=20
        ).pack(pady=10)

    def _cargar_ofertas(self):
        periodo = self.periodo_service.obtener_periodo_activo()
        if not periodo:
            messagebox.showwarning("Advertencia", "No existe un período activo")
            return

        ofertas = self.oferta_service._leer_ofertas()
        ofertas_periodo = [
            o for o in ofertas if o.periodo == periodo.nombre
        ]

        self.texto.configure(state="normal")
        self.texto.delete("1.0", tk.END)

        if not ofertas_periodo:
            self.texto.insert(tk.END, "No existen ofertas académicas registradas.\n")
        else:
            for o in ofertas_periodo:
                linea = (
                    f"{o.codigo_carrera} | "
                    f"{o.nombre_carrera} | "
                    f"{o.canton} | "
                    f"{o.modalidad} | "
                    f"{o.jornada} | "
                    f"Cupos: {o.cupos_disponibles}/{o.total_cupos}\n"
                )
                self.texto.insert(tk.END, linea)

        self.texto.configure(state="disabled")
