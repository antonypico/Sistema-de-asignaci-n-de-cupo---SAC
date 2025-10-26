import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import BOLD
import util.genericos as utl
from forms.form_master import VentanaBienvenida

# Aqui defino la clase que abrira la ventana del login
class VentanaLogin:

    #metodo donde se verifia el usuario y la contraseña
    def verificar(self):
        usu=self.usuario.get()
        contraseña = self.contraseña.get()
        if (usu == "Admin" and contraseña == "12345") or (usu == "Admin_2" and contraseña == "Administrador_2"):
            self.root.destroy()
            root = tk.Tk()
            app = VentanaBienvenida(root)
            root.mainloop()
        else:
            messagebox.showerror(message="Usuario o contraseña incorrectos")





    def __init__(self, root):
        self.root=root #--> esto es para abrir la ventana de login
        self.root.title("Inicio de sesion - SAC") #--> Aqui se define el titulo que se le da a la ventana
        self.root.geometry("800x560") #--> Aqui el tamaño de la ventana
        self.root.configure(bg= "#ffffff") #--> Aqui el color
        self.root.resizable(width=0,height=0) #--> Esto sirve para que no se modifique el tamaño de la ventana
        utl.centrar_ventana(self.root,650,400) #--> Esto es para abrir la pestaña en el centro sin importar el tamaño de la pantalla de la computadora
        
        

        self.logo = utl.leer_imagen("./imagenes/SAC-LOGO.png", (200, 200)) # Aqui se importa la imagen para el logo

        # Frame del logo
        frame_logo = tk.Frame(self.root, bd = 0, width=300, relief=tk.SOLID,padx=10,pady=10,bg = "#EBEBEB") # esto es para configurar el frame del logo
        frame_logo.pack(side="left",expand=tk.NO,fill=tk.BOTH)
        label = tk.Label(frame_logo,image=self.logo,bg="#EBEBEB")
        label.pack(fill=tk.BOTH, expand=True)

        #Frame del lado izquierdo (Parte inicio de sesion)
        frame_form = tk.Frame(self.root, bd = 0, relief=tk.SOLID,bg = "#fcfcfc")
        frame_form.pack (side="right",expand=tk.YES,fill=tk.BOTH)
        
        frame_form_top = tk.Frame(frame_form,height=50,bd=0,relief=tk.SOLID,bg="#fcfcfc")
        frame_form_top.pack(side="top",fill=tk.X)
        titulo_login = tk.Label(frame_form_top,text="Inicio de sesión",font=('Arial',30),fg="#333333",bg="#fcfcfc",pady=25)
        titulo_login.pack(expand=tk.YES,fill=tk.BOTH)

        #frame de insercion de datos login
        frame_form_fill= tk.Frame(frame_form,height = 50, bd = 0, relief = tk.SOLID , bg="#FFFFFF")
        frame_form_fill.pack(side="bottom",expand=tk.YES,fill=tk.BOTH)
        #aqui se configura el espacio para la insercion de texto que pedira el Usuario
        etiqueta_usuario = tk.Label(frame_form_fill, text="Usuario", font=('Arial',16),fg="#000000",bg="#FFFFFF",anchor="w")
        etiqueta_usuario.pack(fill=tk.X,padx=20,pady=5)
        self.usuario = ttk.Entry(frame_form_fill,font=('Arial',14))
        self.usuario.pack(fill = tk.X, padx = 20, pady = 10)
        #aqui se configura el espacio para la insercion de texto que pedira la contraseña
        etiqueta_contraseña = tk.Label(frame_form_fill, text="Contraseña", font=('Arial',16),fg="#000000",bg="#FFFFFF",anchor="w")
        etiqueta_contraseña.pack(fill=tk.X,padx=20,pady=5)
        self.contraseña = ttk.Entry(frame_form_fill,font=('Arial',14))
        self.contraseña.pack(fill = tk.X, padx = 20, pady = 10)
        self.contraseña.config(show="*") #---> aqui se configura que todo el texto ingresado en contraseña se convierta a *

        #Creacion del boton iniciar sesion
        inicio =tk.Button(frame_form_fill,text="Iniciar Sesion",font=('Arial',14,BOLD),bg="#1C4E80",bd=0,fg="#FFFFFF",command = self.verificar)
        inicio.pack(fill=tk.X,padx=20,pady=20)
        inicio.bind("Return", (lambda event: self.verificar()))
