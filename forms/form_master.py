# interfaz principal provisional del sistema SAC
import tkinter as tk
from util import genericos as utl

class VentanaBienvenida:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Asignación de Cupos Universitarios (SAC)")
        self.root.geometry("800x500")
        self.root.configure(bg="#cfe8ef")
        self.root.resizable(width=0, height=0)

        #Posicionamiento del logo
        self.logo = utl.leer_imagen("./imagenes/SAC-LOGO.png", (200, 200))
        self.label_logo = tk.Label(self.root, image=self.logo, bg="#cfe8ef")
        self.label_logo.pack(pady=(30, 10))  # margen superior e inferior

        # Mensaje de bienvenida
        self.label_bienvenida = tk.Label(self.root,text="¡Bienvenido al Sistema de Asignación de Cupos Universitarios!",bg="#cfe8ef",fg="#003366",font=("Helvetica", 18, "bold"),wraplength=800,justify="center")
        self.label_bienvenida.pack(pady=(20, 40))

        # Boton continuar
        self.boton_continuar = tk.Button(self.root,text="Continuar",command=self.continuar,bg="#007acc",fg="white",font=("Arial", 14, "bold"),activebackground="#005f99",activeforeground="white",cursor="hand2",relief="flat")
        self.boton_continuar.pack(pady=20, ipadx=20, ipady=10)
        
    def continuar(self):
        self.root.destroy()
        import tkinter as tk
        from forms.form_pantalla_principal import VentanaPrincipal
        root = tk.Tk()
        app = VentanaPrincipal(root)
