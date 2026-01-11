import tkinter as tk
from tkinter import ttk
from iu.base.ventana_base import VentanaBase



class MenuPrincipalView(VentanaBase):
    def __init__(self, master=None):
        super().__init__(
            master,
            titulo="Menú Principal - SAC",
            ancho=500,
            alto=500
        )

        self._crear_widgets()

    def _crear_widgets(self):
        contenedor = ttk.Frame(self)
        contenedor.pack(expand=True)

        ttk.Label(
            contenedor,
            text="Menú Principal",
            font=("Arial", 18, "bold")
        ).pack(pady=20)

        opciones = [
            "Registrar Estudiantes",
            "Registrar Ofertas Académicas",
            "Ejecutar Asignación de Cupos",
            "Ver Resultados",
            "Salir"
        ]

        for opcion in opciones:
            ttk.Button(
                contenedor,
                text=opcion,
                width=30
            ).pack(pady=8)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    MenuPrincipalView(root)
    root.mainloop()

