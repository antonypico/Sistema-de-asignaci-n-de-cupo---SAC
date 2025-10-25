# interfaz principal provisional del sistema SAC
import tkinter as tk
from util import genericos as utl

class VentanaPrincipal:
    def __init__(self, root):
        self.root=root
        self.root.title("Bienvenido al sistema de Asignación de Cupos Universitarios")
        fondo_principal = "#cfe8ef"
        self.root.configure(bg=fondo_principal)
        self.root.geometry("900x650")
        self.root.resizable(width=0, height=0)

        self.logo = utl.leer_imagen("./imagenes/SAC-LOGO.png", (200, 200))

        label = tk.Label(self.root, image=self.logo, bg=fondo_principal)
        label.place(x=0, y=0, relwidth=1, relheight=1)