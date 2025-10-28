import json
import tkinter as tk
from tkinter import messagebox

# Clase Estudiante
class Estudiante:
    def __init__(self, id_estudiante, nombre, cedula, correo, telefono, puntaje, carrera_postulada, estado_asignacion):
        self.id_estudiante = id_estudiante
        self.nombre = nombre
        self.cedula = cedula
        self.correo = correo
        self.telefono = telefono
        self.puntaje = puntaje
        self.carrera_postulada = carrera_postulada
        self.estado_asignacion = estado_asignacion

    def consultarResultado(self):
        return f"El estado de asignación del estudiante {self.nombre} es: {self.estado_asignacion}"

    def aceptarCupo(self):
        if self.estado_asignacion.lower() == "asignado":
            return f"{self.nombre} ha aceptado el cupo en {self.carrera_postulada}."
        else:
            return f"{self.nombre} no tiene un cupo asignado para aceptar."

    def rechazarCupo(self):
        if self.estado_asignacion.lower() == "asignado":
            self.estado_asignacion = "rechazado"
            return f"{self.nombre} ha rechazado el cupo en {self.carrera_postulada}."
        else:
            return f"{self.nombre} no tiene un cupo asignado para rechazar."

# Funciones JSON
def guardar_estudiante(estudiante):
    try:
        with open("estudiantes.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append(estudiante.__dict__)

    with open("estudiantes.json", "w") as f:
        json.dump(data, f, indent=4)

def consultar_estudiante_por_cedula(cedula):
    try:
        with open("estudiantes.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        return None

    for e in data:
        if e["cedula"] == cedula:
            return e
    return None

# Interfaz de TKinter
def registrar():
    estudiante = Estudiante(
        id_estudiante=entry_id.get(),
        nombre=entry_nombre.get(),
        cedula=entry_cedula.get(),
        correo=entry_correo.get(),
        telefono=entry_telefono.get(),
        puntaje=entry_puntaje.get(),
        carrera_postulada=entry_carrera.get(),
        estado_asignacion=entry_estado.get()
    )
    guardar_estudiante(estudiante)
    messagebox.showinfo("Éxito", f"Estudiante {estudiante.nombre} registrado correctamente.")
    limpiar_campos()

def consultar():
    cedula = entry_cedula.get()
    e = consultar_estudiante_por_cedula(cedula)
    if e:
        messagebox.showinfo("Resultado", f"Estudiante: {e['nombre']}\nEstado: {e['estado_asignacion']}")
    else:
        messagebox.showerror("Error", "Estudiante no encontrado.")

def limpiar_campos():
    for entry in [entry_id, entry_nombre, entry_cedula, entry_correo, entry_telefono, entry_puntaje, entry_carrera, entry_estado]:
        entry.delete(0, tk.END)

# Configurar ventana
ventana = tk.Tk()
ventana.title("Gestión de Estudiantes")
ventana.geometry("400x500")

tk.Label(ventana, text="Registro de Estudiantes", font=("Arial", 14, "bold")).pack(pady=10)

# Campos de entrada
labels = ["ID", "Nombre", "Cédula", "Correo", "Teléfono", "Puntaje", "Carrera postulada", "Estado asignación"]
entries = []

for text in labels:
    tk.Label(ventana, text=text).pack()
    e = tk.Entry(ventana)
    e.pack(pady=3)
    entries.append(e)

entry_id, entry_nombre, entry_cedula, entry_correo, entry_telefono, entry_puntaje, entry_carrera, entry_estado = entries

# Botones
tk.Button(ventana, text="Registrar", command=registrar, bg="#4CAF50", fg="white", width=15).pack(pady=10)
tk.Button(ventana, text="Consultar", command=consultar, bg="#2196F3", fg="white", width=15).pack(pady=5)
tk.Button(ventana, text="Limpiar", command=limpiar_campos, bg="#f39c12", fg="white", width=15).pack(pady=5)

ventana.mainloop()