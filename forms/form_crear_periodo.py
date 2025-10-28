import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from clases.periodo_academico import PeriodoAcademico


# --- Cargar períodos existentes ---
periodos = PeriodoAcademico.cargar()


# --- Ventana principal ---
root = tk.Tk()
root.title("Sistema de Asignación de Cupo")
root.geometry("900x650")
root.config(bg="#cfe8ef")

# Ruta del logo
ruta_logo = os.path.join(os.path.dirname(__file__), "..", "imagenes", "SAC-LOGO.png")
ruta_logo = os.path.abspath(ruta_logo)

logo = Image.open(ruta_logo).convert("RGBA")
logo = logo.resize((130, 130), Image.Resampling.LANCZOS)
logo_tk = ImageTk.PhotoImage(logo)
tk.Label(root, image=logo_tk, bg="#cfe8ef").place(relx=0.03, rely=0.05, anchor="nw")

# Marco tipo tarjeta
card = tk.Frame(root, bg="#e2f1f8", highlightthickness=2,
                highlightbackground="#1b3b6f", padx=40, pady=40)
card.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(card, text="Sistema de Asignación de Cupo",
         font=("Segoe UI", 22, "bold"), fg="#1b3b6f", bg="#e2f1f8").pack(pady=(0, 20))
tk.Label(card, text="Seleccione una opción para continuar",
         font=("Segoe UI", 12), fg="#2f2f2f", bg="#e2f1f8").pack(pady=(0, 25))


# --- Función para crear botones ---
def crear_boton(texto, comando=None, color="#1b3b6f", hover="#2b4f8a"):
    boton = tk.Button(card, text=texto, font=("Segoe UI Semibold", 13),
                      fg="white", bg=color, activebackground=hover,
                      relief="flat", cursor="hand2", height=2, width=25,
                      command=comando)
    boton.pack(pady=8, fill="x")
    return boton


# --- Crear nuevo período ---
def abrir_ventana_periodo():
    ventana = tk.Toplevel(root)
    ventana.title("Nuevo Período Académico")
    ventana.geometry("400x400")
    ventana.config(bg="#e2f1f8")

    tk.Label(ventana, text="Crear nuevo período académico",
             font=("Segoe UI", 14, "bold"), bg="#e2f1f8", fg="#1b3b6f").pack(pady=10)

    tk.Label(ventana, text="Código:", bg="#e2f1f8").pack()
    entry_codigo = tk.Entry(ventana, width=30)
    entry_codigo.pack(pady=5)

    tk.Label(ventana, text="Fecha inicio (dd/mm/aaaa):", bg="#e2f1f8").pack()
    entry_inicio = tk.Entry(ventana, width=30)
    entry_inicio.pack(pady=5)

    tk.Label(ventana, text="Fecha fin (dd/mm/aaaa):", bg="#e2f1f8").pack()
    entry_fin = tk.Entry(ventana, width=30)
    entry_fin.pack(pady=5)

    tk.Label(ventana, text="Estado (Abierto/Cerrado):", bg="#e2f1f8").pack()
    entry_estado = tk.Entry(ventana, width=30)
    entry_estado.pack(pady=5)

    def crear_periodo():
        codigo = entry_codigo.get()
        f_inicio = entry_inicio.get()
        f_fin = entry_fin.get()
        estado_input = entry_estado.get()

        inicio, fin, error_fechas = PeriodoAcademico.validar_fechas(f_inicio, f_fin)
        if error_fechas:
            messagebox.showwarning("Error", error_fechas)
            return

        estado, error_estado = PeriodoAcademico.validar_estado(estado_input)
        if error_estado:
            messagebox.showwarning("Error", error_estado)
            return

        # Verificar si ya existe un período con ese código
        for p in periodos:
            if p.codigo == codigo:
                messagebox.showwarning("Error", "Ya existe un período con ese código.")
                return

        nuevo = PeriodoAcademico(codigo, inicio, fin, estado)
        periodos.append(nuevo)
        PeriodoAcademico.guardar(periodos)

        messagebox.showinfo("Éxito", "Período académico guardado correctamente.")
        ventana.destroy()

    tk.Button(ventana, text="Guardar Período", bg="#1b3b6f", fg="white",
              relief="flat", width=20, command=crear_periodo).pack(pady=20)


# --- Mostrar períodos ---
def mostrar_periodos():
    if not periodos:
        messagebox.showinfo("Información", "No hay períodos registrados.")
        return

    ventana = tk.Toplevel(root)
    ventana.title("Lista de Períodos Académicos")
    ventana.geometry("450x400")
    ventana.config(bg="#e2f1f8")

    tk.Label(ventana, text="Períodos guardados:",
             font=("Segoe UI", 14, "bold"), bg="#e2f1f8", fg="#1b3b6f").pack(pady=10)

    lista = tk.Listbox(ventana, width=60, height=12)
    lista.pack(pady=10)

    for p in periodos:
        texto = f"{p.codigo} | {p.fecha_inicio.strftime('%d/%m/%Y')} - {p.fecha_fin.strftime('%d/%m/%Y')} | {p.estado}"
        lista.insert(tk.END, texto)


# Botones principales
crear_boton("Crear nuevo período", comando=abrir_ventana_periodo)
crear_boton("Ver períodos guardados", comando=mostrar_periodos)
crear_boton("Configurar carrera")
crear_boton("Cargar archivo")
crear_boton("Ver resultados")
crear_boton("Exportar resultados")

# Botón Salir
tk.Button(card, text="Salir", font=("Segoe UI Semibold", 13),
          fg="white", bg="#d9534f", activebackground="#c9302c",
          relief="flat", cursor="hand2", height=2, width=25,
          command=root.destroy).pack(pady=20, fill="x")

# Pie
tk.Label(root, text="© 2025 Sistema Académico - SAC",
         font=("Segoe UI", 9), fg="#1b3b6f", bg="#cfe8ef").pack(side="bottom", pady=10)

root.mainloop()
