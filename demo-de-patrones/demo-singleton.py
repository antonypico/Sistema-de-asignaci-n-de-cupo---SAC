import json
from datetime import datetime


class GestionPeriodo:
    """
    Clase encargada de la gestión de períodos académicos.
    Implementa el patrón Singleton (patrón creacional)
    para garantizar que exista una sola instancia.
    """

    # Atributo de clase que almacena la única instancia (Singleton)
    _instancia = None

    # Nombre del archivo donde se guardan los períodos
    ARCHIVO = "periodos.json"

    def __new__(cls):
        """
        Método especial que controla la creación de la instancia.
        Si no existe una instancia, se crea y se cargan los períodos.
        """
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            # Carga inicial de los períodos desde el archivo JSON
            cls._instancia.periodos = cls._instancia.cargar_periodos()
        return cls._instancia

    def cargar_periodos(self):
        """
        Carga los períodos académicos desde el archivo JSON.
        Si el archivo no existe, retorna una lista vacía.
        """
        try:
            with open(self.ARCHIVO, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def guardar_periodo(self):
        """
        Guarda la lista actual de períodos en el archivo JSON.
        """
        with open(self.ARCHIVO, "w", encoding="utf-8") as f:
            json.dump(self.periodos, f, indent=4, ensure_ascii=False)
        print("Períodos guardados correctamente.")

    def agregar_periodo(self, nombre, inicio, fin):
        """
        Agrega un nuevo período académico.
        Valida formato de fechas, coherencia de fechas y duplicados.
        """
        # Limpia espacios innecesarios
        nombre = nombre.strip()
        inicio = inicio.strip()
        fin = fin.strip()

        # Validación de fechas
        try:
            inicio_dt = datetime.strptime(inicio, "%d-%m-%Y")
            fin_dt = datetime.strptime(fin, "%d-%m-%Y")
            if fin_dt < inicio_dt:
                print("La fecha de fin no puede ser anterior a la de inicio.")
                return
        except ValueError:
            print("Formato de fecha incorrecto. Use DD-MM-AAAA.")
            return

        # Verifica que no exista un período con el mismo nombre
        if any(p["nombre"] == nombre for p in self.periodos):
            print(f"Ya existe un período con el nombre '{nombre}'.")
            return

        # Agrega el nuevo período a la lista
        self.periodos.append({
            "nombre": nombre,
            "inicio": inicio,
            "fin": fin
        })

        print(f"Período '{nombre}' agregado.")
        self.guardar_periodo()

    def listar_periodo(self):
        """
        Muestra en pantalla todos los períodos registrados.
        """
        if not self.periodos:
            print("No hay períodos registrados.")
            return

        print("Lista de períodos académicos:")
        for p in self.periodos:
            print(f"- {p['nombre']}: {p['inicio']} → {p['fin']}")


def mostrar_menu():
    """
    Muestra el menú principal del sistema.
    """
    print("\nGestión de Períodos")
    print("1. Listar períodos")
    print("2. Agregar período")
    print("3. Salir")


def main():
    """
    Función principal del programa.
    Controla el flujo del menú y la interacción con el usuario.
    """
    # Se obtiene la única instancia del gestor (Singleton)
    gestor = GestionPeriodo()

    while True:
        mostrar_menu()
        opcion = input("Elija una opción (1-3): ").strip()

        if opcion == "1":
            gestor.listar_periodo()
        elif opcion == "2":
            nombre = input("Nombre del período: ")
            inicio = input("Fecha inicio (DD-MM-AAAA): ")
            fin = input("Fecha fin (DD-MM-AAAA): ")
            gestor.agregar_periodo(nombre, inicio, fin)
        elif opcion == "3":
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")


# Punto de entrada del programa
if __name__ == "__main__":
    main()
