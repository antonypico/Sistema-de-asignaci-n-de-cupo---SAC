import tkinter as tk
from tkinter import ttk
from iu.base.ventana_base import VentanaBase



class LoginView(VentanaBase):
    def __init__(self, master=None):
        super().__init__(
            master,
            titulo="Login - SAC",
            ancho=450,
            alto=350
        )

        self._crear_widgets()

    def _crear_widgets(self):
        contenedor = ttk.Frame(self)
        contenedor.pack(expand=True)

        ttk.Label(
            contenedor,
            text="Sistema de Asignación de Cupos",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        ttk.Label(contenedor, text="Usuario").pack(anchor="w")
        ttk.Entry(contenedor, width=30).pack(pady=5)

        ttk.Label(contenedor, text="Contraseña").pack(anchor="w")
        ttk.Entry(contenedor, width=30, show="*").pack(pady=5)

        ttk.Button(
            contenedor,
            text="Iniciar Sesión",
            width=25
        ).pack(pady=20)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    LoginView(root)
    root.mainloop()

