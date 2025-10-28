import tkinter as tk
from PIL import Image, ImageTk
from forms.form_ventana_periodo import VentanaPeriodo


class VentanaPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Asignación de Cupo")
        self.root.geometry("900x650")
        self.root.config(bg="#cfe8ef")

        # --- Logo ---
        ruta_logo = "imagenes/SAC-LOGO.png"  # Ruta directa
        logo = Image.open(ruta_logo).convert("RGBA")
        logo = logo.resize((130, 130), Image.Resampling.LANCZOS)
        logo_tk = ImageTk.PhotoImage(logo)

        lbl_logo = tk.Label(self.root, image=logo_tk, bg="#cfe8ef", bd=0)
        lbl_logo.image = logo_tk
        lbl_logo.place(relx=0.03, rely=0.05, anchor="nw")

        # --- Marco tipo tarjeta ---
        card = tk.Frame(self.root,bg="#e2f1f8",bd=0,highlightthickness=2,highlightbackground="#1b3b6f",padx=40,pady=40)
        card.place(relx=0.5, rely=0.5, anchor="center")

        # --- Título ---
        titulo = tk.Label(card,text="Sistema de Asignación de Cupo",font=("Segoe UI", 22, "bold"),fg="#1b3b6f",bg="#e2f1f8")
        titulo.pack(pady=(0, 20))

        # --- Subtítulo ---
        subtitulo = tk.Label(card,text="Seleccione una opción para continuar",font=("Segoe UI", 12),fg="#2f2f2f",bg="#e2f1f8")
        subtitulo.pack(pady=(0, 25))

        # --- Función para crear botones ---
        def crear_boton(texto, color="#1b3b6f", hover="#2b4f8a", comando=None):
            boton = tk.Button(card,text=texto,font=("Segoe UI Semibold", 13),fg="white",bg=color,activebackground=hover,activeforeground="white",relief="flat",bd=0,cursor="hand2",height=2,width=25,command=comando)
            boton.pack(pady=8, fill="x")
            return boton
        

        # --- Botones principales ---
        crear_boton("Crear nuevo período", comando=self.abrir_ventana_periodo)
        crear_boton("Configurar carrera")
        crear_boton("Cargar archivo")
        crear_boton("Ver resultados")
        crear_boton("Exportar resultados")

        # --- Botón Salir ---
        btn_salir = tk.Button(card,text="Salir",font=("Segoe UI Semibold", 13),fg="white",bg="#d9534f",activebackground="#c9302c",activeforeground="white",relief="flat",bd=0,cursor="hand2",height=2,width=25,command=self.root.destroy)
        btn_salir.pack(pady=20, fill="x")

        # --- Pie de página ---
        footer = tk.Label(self.root,text="© 2025 Sistema Académico - SAC - Hecho por el equipo ",font=("Segoe UI", 9),fg="#1b3b6f",bg="#cfe8ef")
        footer.pack(side="bottom", pady=10)

    
        
    def abrir_ventana_periodo(self):
        VentanaPeriodo(self.root)

