import tkinter as tk
from tkinter import messagebox
from clases.periodo_academico import PeriodoAcademico

class PanelEliminarPeriodo(tk.Frame):
    def __init__(self, master, actualizar_lista_callback, **kwargs):
        super().__init__(master, **kwargs)
        self.actualizar_lista_callback = actualizar_lista_callback
        self.config(bg="#f7f7f7")
        self.crear_widgets()

    def crear_widgets(self):
        self.actualizar_lista()

    def actualizar_lista(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.periodos = PeriodoAcademico.cargar()
        if not self.periodos:
            tk.Label(self, text="No hay períodos para eliminar", bg="#f7f7f7").pack()
            return

        tk.Label(self, text="Seleccione un período a eliminar:", bg="#f7f7f7").pack(pady=5)
        self.var_seleccion = tk.StringVar(value="")

        for p in self.periodos:
            tk.Radiobutton(self, text=f"{p.nombre} ({p.fecha_inicio} - {p.fecha_fin})",
                           variable=self.var_seleccion, value=p.nombre,
                           bg="#f7f7f7", anchor="w").pack(fill="x")

        tk.Button(self, text="Eliminar", bg="#d9534f", fg="white",
                  command=self.eliminar_periodo).pack(pady=10)

    def eliminar_periodo(self):
        nombre = self.var_seleccion.get()
        if not nombre:
            messagebox.showerror("Error", "Seleccione un período")
            return
        periodos_nuevos = [p for p in self.periodos if p.nombre != nombre]
        PeriodoAcademico.guardar(periodos_nuevos)
        messagebox.showinfo("Éxito", f"Período '{nombre}' eliminado")
        self.actualizar_lista_callback()
