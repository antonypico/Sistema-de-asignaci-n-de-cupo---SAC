import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import BOLD
import util.genericos as utl
from forms.form_master import VentanaBienvenida

class VentanaLogin:

#Clase para la interfaz del login

    def __init__(self, root):
        # Ventana principal
        self.root = root
        self.root.title("Inicio de sesión - SAC")
        self.root.geometry("800x560")
        self.root.configure(bg="#ffffff")
        self.root.resizable(width=0, height=0)
        utl.centrar_ventana(self.root, 650, 400)

        # Cargo el logo
        self.logo = utl.leer_imagen("./imagenes/SAC-LOGO.png", (200, 200))

        # Armo toda la interfaz
        self._crear_interfaz()


    # Métodos de los frames


    def _crear_interfaz(self): 
        #Crea los frames y widgets del login
        self._crear_frame_logo()
        self._crear_frame_formulario()

    def _crear_frame_logo(self):
        #Frame izquierdo con el logo
        frame_logo = tk.Frame(self.root, bd=0, width=300, relief=tk.SOLID, padx=10, pady=10, bg="#EBEBEB")
        frame_logo.pack(side="left", expand=tk.NO, fill=tk.BOTH)

        label_logo = tk.Label(frame_logo, image=self.logo, bg="#EBEBEB")
        label_logo.pack(fill=tk.BOTH, expand=True)

    def _crear_frame_formulario(self):
        #Frame derecho con los campos de login
        frame_form = tk.Frame(self.root, bd=0, relief=tk.SOLID, bg="#fcfcfc")
        frame_form.pack(side="right", expand=tk.YES, fill=tk.BOTH)

        # Parte superior: título
        frame_top = tk.Frame(frame_form, height=50, bd=0, bg="#fcfcfc")
        frame_top.pack(side="top", fill=tk.X)

        titulo = tk.Label(
            frame_top,
            text="Inicio de sesión",
            font=('Arial', 30),
            fg="#333333",
            bg="#fcfcfc",
            pady=25
        )
        titulo.pack(expand=tk.YES, fill=tk.BOTH)

        # Parte inferior: formulario
        frame_bottom = tk.Frame(frame_form, height=50, bd=0, bg="#FFFFFF")
        frame_bottom.pack(side="bottom", expand=tk.YES, fill=tk.BOTH)

        # Usuario
        tk.Label(
            frame_bottom, text="Usuario", font=('Arial', 16),
            fg="#000000", bg="#FFFFFF", anchor="w"
        ).pack(fill=tk.X, padx=20, pady=5)

        self.usuario = ttk.Entry(frame_bottom, font=('Arial', 14))
        self.usuario.pack(fill=tk.X, padx=20, pady=10)

        # Contraseña
        tk.Label(
            frame_bottom, text="Contraseña", font=('Arial', 16),
            fg="#000000", bg="#FFFFFF", anchor="w"
        ).pack(fill=tk.X, padx=20, pady=5)

        self.contraseña = ttk.Entry(frame_bottom, font=('Arial', 14), show="*")
        self.contraseña.pack(fill=tk.X, padx=20, pady=10)

        # Botón de inicio de sesión
        boton_login = tk.Button(
            frame_bottom,
            text="Iniciar Sesión",
            font=('Arial', 14, BOLD),
            bg="#1C4E80",
            bd=0,
            fg="#FFFFFF",
            command=self.verificar_usuario
        )
        boton_login.pack(fill=tk.X, padx=20, pady=20)
        boton_login.bind("<Return>", lambda event: self.verificar_usuario())

    # Métodos de lógica

    def verificar_usuario(self):
        #Verifica si el usuario y contraseña son correctos
        usuario = self.usuario.get().strip()
        contraseña = self.contraseña.get().strip()

        if self._credenciales_validas(usuario, contraseña):
            self._abrir_ventana_bienvenida()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def _credenciales_validas(self, usuario, contraseña):
        #Comprueba las credenciales (se puede mejorar con BD después)
        usuarios_validos = {
            "Admin": "12345",
            "Admin_2": "Administrador_2"
        }
        return usuarios_validos.get(usuario) == contraseña

    def _abrir_ventana_bienvenida(self):
        #Abre la ventana principal después del login
        self.root.destroy()
        root = tk.Tk()
        VentanaBienvenida(root)
        root.mainloop()
