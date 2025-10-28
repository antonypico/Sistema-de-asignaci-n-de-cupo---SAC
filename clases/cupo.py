import json
import os
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime


DATA_FILE = "asignaciones.json"


class AsignacionCupo:
    def __init__(self, id_asignacion, estudiante, carrera, fecha_asignacion, estado):
        self.id_asignacion = id_asignacion
        self.estudiante = estudiante
        self.carrera = carrera
        self.fecha_asignacion = fecha_asignacion
        self.estado = estado

    def to_dict(self):
        return {
            "id_asignacion": self.id_asignacion,
            "estudiante": self.estudiante,
            "carrera": self.carrera,
            "fecha_asignacion": self.fecha_asignacion,
            "estado": self.estado
        }


class GestorAsignaciones:

    @staticmethod
    def cargar_datos():
        if not os.path.exists(DATA_FILE):
            return []
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def guardar_datos(data):
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    @staticmethod
    def asignar_cupo(estudiante, carrera):
        data = GestorAsignaciones.cargar_datos()

        nuevo_id = len(data) + 1
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        asignacion = AsignacionCupo(
            nuevo_id,
            estudiante,
            carrera,
            fecha_actual,
            "Activo"
        )
        data.append(asignacion.to_dict())
        GestorAsignaciones.guardar_datos(data)

    @staticmethod
    def anular_asignacion(id_asignacion):
        data = GestorAsignaciones.cargar_datos()
        for asignacion in data:
            if asignacion["id_asignacion"] == id_asignacion:
                asignacion["estado"] = "Anulado"
        GestorAsignaciones.guardar_datos(data)


class InterfazTk:
    def __init__(self, root):
        self.root = root
        root.title("Asignación de Cupos")

        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        tk.Label(self.frame, text="Estudiante").grid(row=0, column=0)
        self.entry_est = tk.Entry(self.frame)
        self.entry_est.grid(row=0, column=1)

        tk.Label(self.frame, text="Carrera").grid(row=1, column=0)
        self.entry_car = tk.Entry(self.frame)
        self.entry_car.grid(row=1, column=1)

        tk.Button(self.frame, text="Asignar Cupo", command=self.asignar).grid(row=2, column=0, columnspan=2, pady=5)

        self.tree = ttk.Treeview(root, columns=("ID","Estudiante","Carrera","Fecha","Estado"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack()

        tk.Button(root, text="Actualizar Lista", command=self.cargar_tabla).pack(pady=3)
        tk.Button(root, text="Anular Seleccionado", command=self.anular).pack(pady=3)

        self.cargar_tabla()

    def asignar(self):
        estudiante = self.entry_est.get().strip()
        carrera = self.entry_car.get().strip()
        if estudiante == "" or carrera == "":
            messagebox.showwarning("Error", "Faltan datos")
            return

        GestorAsignaciones.asignar_cupo(estudiante, carrera)
        self.entry_est.delete(0, tk.END)
        self.entry_car.delete(0, tk.END)
        self.cargar_tabla()
        messagebox.showinfo("Éxito", "Cupo asignado correctamente")

    def cargar_tabla(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        data = GestorAsignaciones.cargar_datos()
        for a in data:
            self.tree.insert("", tk.END, values=(a["id_asignacion"], a["estudiante"], a["carrera"], a["fecha_asignacion"], a["estado"]))

    def anular(self):
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Error", "Seleccione una asignación")
            return
        id_asignacion = int(self.tree.item(item, "values")[0])
        GestorAsignaciones.anular_asignacion(id_asignacion)
        self.cargar_tabla()
        messagebox.showinfo("Éxito", "Asignación anulada")


if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazTk(root)
    root.mainloop()
