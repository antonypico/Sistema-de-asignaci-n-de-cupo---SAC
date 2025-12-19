# interfaz principal provisional del sistema SAC
import tkinter as tk
from util import genericos as utl
from forms.form_pantalla_principal import VentanaPrincipal


class VentanaBienvenida:


    def __init__(self, root):
        # Configuración básica de la ventana
        self.root = root
        self.root.title("Sistema de Asignación de Cupos Universitarios (SAC)")
        self.root.geometry("800x500")
        self.root.configure(bg="#cfe8ef")
        self.root.resizable(width=0, height=0)
        utl.centrar_ventana(self.root, 800, 500)

        # Cargo el logo
        self.logo = utl.leer_imagen("./imagenes/SAC-LOGO.png", (200, 200))

        # Armo toda la interfaz
        self._crear_interfaz()


    # Métodos internos (solo de la interfaz)


    def _crear_interfaz(self):
        #Crea los elementos gráficos de la ventana de bienvenida"""
        self._crear_logo()
        self._crear_mensaje_bienvenida()
        self._crear_boton_continuar()

    def _crear_logo(self):
        """Muestra el logo del sistema en la parte superior"""
        label_logo = tk.Label(self.root, image=self.logo, bg="#cfe8ef")
        label_logo.pack(pady=(30, 10))

    def _crear_mensaje_bienvenida(self):
        """Muestra el mensaje principal"""
        label_bienvenida = tk.Label(
            self.root,
            text="¡Bienvenido al Sistema de Asignación de Cupos Universitarios!",
            bg="#cfe8ef",
            fg="#003366",
            font=("Helvetica", 18, "bold"),
            wraplength=800,
            justify="center"
        )
        label_bienvenida.pack(pady=(20, 40))

    def _crear_boton_continuar(self):
        """Crea el botón para avanzar a la pantalla principal"""
        boton_continuar = tk.Button(
            self.root,
            text="Continuar",
            command=self._abrir_pantalla_principal,
            bg="#007acc",
            fg="white",
            font=("Arial", 14, "bold"),
            activebackground="#005f99",
            activeforeground="white",
            cursor="hand2",
            relief="flat"
        )
        boton_continuar.pack(pady=20, ipadx=20, ipady=10)

    # Métodos de lógica
 
    def _abrir_pantalla_principal(self):
        """Cierra esta ventana y abre la interfaz principal"""
        self.root.destroy()
        root = tk.Tk()
        VentanaPrincipal(root)
        root.mainloop()
