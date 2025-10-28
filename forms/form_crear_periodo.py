# forms/panel_crear_periodo.py
import tkinter as tk
from tkinter import messagebox
from clases.periodo_academico import PeriodoAcademico

class PanelCrearPeriodo(tk.Frame):
    def __init__(self, master, actualizar_lista_callback, **kwargs):
        super().__init__(master, **kwargs)
        self.actualizar_lista_callback = actualizar_lista_callback
        self.config(bg="#f7f7f7")
        self.crear_widgets()

    def crear_widgets(self):
        tk.Label(self, text="Nombre del período:", bg="#f7f7f7").pack(pady=5)
        self.entry_nombre = tk.Entry(self)
        self.entry_nombre.pack(pady=5)

        tk.Label(self, text="Fecha inicio (YYYY-MM-DD):", bg="#f7f7f7").pack(pady=5)
        self.entry_inicio = tk.Entry(self)
        self.entry_inicio.pack(pady=5)

        tk.Label(self, text="Fecha fin (YYYY-MM-DD):", bg="#f7f7f7").pack(pady=5)
        self.entry_fin = tk.Entry(self)
        self.entry_fin.pack(pady=5)

        tk.Button(self, text="Guardar", bg="#1b3b6f", fg="white",
                  command=self.guardar_periodo).pack(pady=20)

    def guardar_periodo(self):
        nombre = self.entry_nombre.get()
        inicio = self.entry_inicio.get()
        fin = self.entry_fin.get()
        if not nombre or not inicio or not fin:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        PeriodoAcademico.agregar_periodo(nombre, inicio, fin)
        messagebox.showinfo("Éxito", f"Período '{nombre}' creado correctamente")
        self.actualizar_lista_callback()