import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from iu.base.ventana_base import VentanaBase
from services.periodo_service import PeriodoService


class CrearPeriodoView(VentanaBase):
    def __init__(self, master=None):
        super().__init__(
            master,
            titulo="Crear Período Académico",
            ancho=450,
            alto=350
        )
        
        self.periodo_service = PeriodoService()
        self._crear_widgets()

    def _crear_widgets(self):
        contenedor = ttk.Frame(self)
        contenedor.pack(expand=True, padx=20,pady=20)
        
        ttk.Label(
            contenedor,
            text="Nuevo Período Académico",
            font=("Arial", 16, "bold")
        ).pack(pady=15)
        
        #Nombre del periodo
        ttk.Label(contenedor, text="Período: (0000-00-00)").pack(anchor="w")
        self.entry_nombre = ttk.Entry(contenedor, width=30)
        self.entry_nombre.pack(pady=5)
        
        #Fecha inicio
        ttk.Label(contenedor, text="Fecha inicio: (0000-00-00)").pack(anchor="w")
        self.entry_inicio = ttk.Entry(contenedor, width=30)
        self.entry_inicio.pack(pady=5)

        #Fecha fin
        ttk.Label(contenedor, text="Fecha fin: (0000-00-00)").pack(anchor="w")
        self.entry_fin = ttk.Entry(contenedor, width=30)
        self.entry_fin.pack(pady=5)
        
        frame_botones = ttk.Frame(contenedor)
        frame_botones.pack(pady=20)

        ttk.Button(
            frame_botones,
            text="Cancelar",
            command=self.destroy
        ).pack(side="left", padx=10)
        
    def _guardar_periodo(self):
        nombre = self.entry_nombre.get().strip()
        inicio_txt = self.entry_inicio.get().strip()
        fin_txt = self.entry_fin.get().strip()

        if not nombre or not inicio_txt or not fin_txt:
            messagebox.showwarning(
                "Advertencia",
                "Debe completar todos los campos"
            )
            return

        try:
            fecha_inicio = date.fromisoformat(inicio_txt)
            fecha_fin = date.fromisoformat(fin_txt)
        except ValueError:
            messagebox.showerror(
                "Error",
                "Las fechas deben tener formato YYYY-MM-DD"
            )
            return

        if fecha_inicio > fecha_fin:
            messagebox.showerror(
                "Error",
                "La fecha de inicio no puede ser mayor que la fecha de fin"
            )
            return

        try:
            self.periodo_service.crear_periodo(
                nombre,
                fecha_inicio,
                fecha_fin
            )

            messagebox.showinfo(
                "Éxito",
                f"Período {nombre} creado correctamente"
            )
            self.destroy()

        except ValueError as e:
            messagebox.showwarning(
                "Advertencia",
                str(e)
            )
            return
        