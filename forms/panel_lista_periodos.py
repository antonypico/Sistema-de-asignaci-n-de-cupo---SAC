# forms/panel_lista_periodos.py
import tkinter as tk
from clases.periodo_academico import PeriodoAcademico

class PanelListaPeriodos(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.config(bg="#f7f7f7")
        self.actualizar_lista()

    def actualizar_lista(self):
        for widget in self.winfo_children():
            widget.destroy()
        periodos = PeriodoAcademico.cargar()
        if not periodos:
            tk.Label(self, text="No hay períodos disponibles", bg="#f7f7f7").pack()
            return
        for p in periodos:
            tk.Label(self, text=f"{p.nombre} ({p.fecha_inicio} - {p.fecha_fin})",
                     bg="#f7f7f7", anchor="w").pack(fill="x")
