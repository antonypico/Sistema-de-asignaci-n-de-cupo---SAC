import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import BOLD
import util.genericos as utl
from forms.form_master import VentanaPrincipal

class VentanaLogin:
    def __init__(self, root):
        self.root=root
        self.root.title("Inicio de sesion - SAC")
        self.root.geometry("800x560")
        self.root.configure(bg= "#ffffff")
        self.root.resizable(width=0,height=0)
        utl.centrar_ventana(self.root,650,400)
        
        

        self.logo = utl.leer_imagen("./imagenes/SAC-LOGO.png", (200, 200))

        # Frame del logo
        frame_logo = tk.Frame(self.root, bd = 0, width=300, relief=tk.SOLID,padx=10,pady=10,bg = "#cfe8ef")
        frame_logo.pack(side="left",expand=tk.NO,fill=tk.BOTH)
        label = tk.Label(frame_logo,image=self.logo,bg="#cfe8ef")
        label.pack(fill=tk.BOTH, expand=True)

        #Frame del lado izquierdo (Parte inicio de seson)
        frame_form = tk.Frame(self.root, bd = 0, relief=tk.SOLID,bg = "#fcfcfc")
        frame_form.pack (side="right",expand=tk.YES,fill=tk.BOTH)
        
        frame_form_top = tk.Frame(frame_form,height=50,bd=0,relief=tk.SOLID,bg="Black")
        frame_form_top.pack(side="top",fill=tk.X)
        titulo_login = tk.Label(frame_form_top,text="Inicio de sesión",font=('Times',30),fg="#000000",bg="#fcfcfc",pady=25)
        titulo_login.pack(expand=tk.YES,fill=tk.BOTH)