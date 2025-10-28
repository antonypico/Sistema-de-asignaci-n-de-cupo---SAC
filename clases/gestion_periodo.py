import json
from datetime import datetime

class GestionPeriodo:
    ARCHIVO = "periodos.json"

    def __init__(self):
        self.periodos = self.cargar_periodos()

    def cargar_periodos(self):
        try:
            with open(self.ARCHIVO, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def guardar_periodo(self):
        with open(self.ARCHIVO, "w") as f:
            json.dump(self.periodos, f, indent=4)
        print("Períodos guardados correctamente.")

    def agregar_periodo(self, nombre, inicio, fin):
        nombre = nombre.strip()
        inicio = inicio.strip()
        fin = fin.strip()

        try:
            inicio_dt = datetime.strptime(inicio, "%d-%m-%Y")
            fin_dt = datetime.strptime(fin, "%d-%m-%Y")
            if fin_dt < inicio_dt:
                print("La fecha de fin no puede ser anterior a la de inicio.")
                return
        except ValueError:
            print("Formato de fecha incorrecto. Use DD-MM-AAAA.")
            return

        if any(p["nombre"] == nombre for p in self.periodos):
            print(f"Ya existe un período con el nombre '{nombre}'.")
            return

        self.periodos.append({"nombre": nombre, "inicio": inicio, "fin": fin})
        print(f"Período '{nombre}' agregado.")

    def listar_periodo(self):
        if not self.periodos:
            print("No hay períodos registrados.")
            return

        print("Lista de períodos académicos:")
        for p in self.periodos:
            print(f"- {p['nombre']}: {p['inicio']} → {p['fin']}")

