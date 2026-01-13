import tkinter as tk
from tkinter import ttk, messagebox

from iu.base.ventana_base import VentanaBase
from iu.menu.form_menu_principal import MenuPrincipalView


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
        contenedor.pack(expand=True, padx=20, pady=20)

        ttk.Label(
            contenedor,
            text="Sistema de Asignación de Cupos",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        ttk.Label(contenedor, text="Usuario").pack(anchor="w")
        self.entry_usuario = ttk.Entry(contenedor, width=30)
        self.entry_usuario.pack(pady=5)

        ttk.Label(contenedor, text="Contraseña").pack(anchor="w")
        self.entry_clave = ttk.Entry(contenedor, width=30, show="*")
        self.entry_clave.pack(pady=5)

        ttk.Button(
            contenedor,
            text="Iniciar Sesión",
            width=25,
            command=self._validar_login
        ).pack(pady=20)

    def _validar_login(self):
        usuario = self.entry_usuario.get()
        clave = self.entry_clave.get()

        # Credenciales fijas (suficientes para el proyecto)
        if usuario == "admin" and clave == "admin123":
            self.destroy()
            MenuPrincipalView(self.master)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    LoginView(root)
    root.mainloop()
