# forms/form_crear_periodo.py
import tkinter as tk
from tkinter import messagebox
from clases.periodo_academico import PeriodoAcademico

class CrearPeriodo:
    def __init__(self, root):
        self.root = root
        self.root.title("Crear Nuevo Período")
        self.root.geometry("400x300")
        self.root.config(bg="#cfe8ef")

        tk.Label(root, text="Nombre del período:", bg="#cfe8ef").pack(pady=5)
        self.entry_nombre = tk.Entry(root)
        self.entry_nombre.pack(pady=5)

        tk.Label(root, text="Fecha de inicio (YYYY-MM-DD):", bg="#cfe8ef").pack(pady=5)
        self.entry_inicio = tk.Entry(root)
        self.entry_inicio.pack(pady=5)

        tk.Label(root, text="Fecha de fin (YYYY-MM-DD):", bg="#cfe8ef").pack(pady=5)
        self.entry_fin = tk.Entry(root)
        self.entry_fin.pack(pady=5)

        tk.Button(root, text="Guardar", bg="#1b3b6f", fg="white", command=self.guardar_periodo).pack(pady=20)

    def guardar_periodo(self):
        nombre = self.entry_nombre.get()
        inicio = self.entry_inicio.get()
        fin = self.entry_fin.get()

        if not nombre or not inicio or not fin:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        PeriodoAcademico.agregar_periodo(nombre, inicio, fin)
        messagebox.showinfo("Éxito", f"Período '{nombre}' creado correctamente")
        self.root.destroy()
