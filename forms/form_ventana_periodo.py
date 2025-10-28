import tkinter as tk
from tkinter import messagebox


class VentanaPeriodo:
    def __init__(self, master):
        # Crear nueva ventana secundaria
        self.ventana = tk.Toplevel(master)
        self.ventana.title("Gestión de Períodos")
        self.ventana.geometry("500x400")
        self.ventana.config(bg="#e2f1f8")

        # --- Marco principal ---
        frame = tk.Frame(self.ventana, bg="#ffffff", bd=0,
                         highlightthickness=2, highlightbackground="#1b3b6f",
                         padx=30, pady=30)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # --- Título ---
        titulo = tk.Label(frame, text="Gestión de Períodos",
                          font=("Segoe UI", 18, "bold"),
                          fg="#1b3b6f", bg="#ffffff")
        titulo.pack(pady=(0, 20))

        # --- Función auxiliar para botones ---
        def crear_boton(texto, comando=None):
            boton = tk.Button(
                frame, text=texto, font=("Segoe UI Semibold", 12),
                fg="white", bg="#1b3b6f", activebackground="#2b4f8a",
                activeforeground="white", relief="flat", bd=0,
                cursor="hand2", height=2, width=20, command=comando
            )
            boton.pack(pady=8)
            return boton

        # --- Botones de acción ---
        crear_boton("Crear período", comando=self.crear_periodo)
        crear_boton("Eliminar período", comando=self.eliminar_periodo)
        crear_boton("Listar períodos", comando=self.listar_periodos)

        # --- Botón cerrar ---
        btn_cerrar = tk.Button(frame, text="Cerrar", font=("Segoe UI Semibold", 12),
                               fg="white", bg="#d9534f", activebackground="#c9302c",
                               activeforeground="white", relief="flat", bd=0,
                               cursor="hand2", height=2, width=20,
                               command=self.ventana.destroy)
        btn_cerrar.pack(pady=(20, 0))

   
    def crear_periodo(self):
    # Función para abrir el panel de creación de período
        def actualizar_lista_dummy():
            # Por ahora solo un ejemplo de callback
            print("Lista de períodos actualizada")

    # Crear nueva ventana para el panel
        ventana_crear = tk.Toplevel(self.ventana)
        ventana_crear.title("Crear Período")
        ventana_crear.geometry("400x350")
        ventana_crear.config(bg="#f7f7f7")

    # Importar y agregar el panel
        from forms.panel_crear_periodo import PanelCrearPeriodo
        panel = PanelCrearPeriodo(ventana_crear, actualizar_lista_callback=actualizar_lista_dummy)
        panel.pack(expand=True, fill="both")


    def eliminar_periodo(self):
        messagebox.showinfo("Eliminar", "Aquí se eliminará un período")

    def listar_periodos(self):
        messagebox.showinfo("Listar", "Aquí se listarán los períodos")
