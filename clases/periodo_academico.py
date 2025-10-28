import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime
import os

# --- Clase POO ---
class PeriodoAcademico:
    def __init__(self, codigo, fecha_inicio, fecha_fin, estado):
        self.codigo = codigo
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.estado = estado

    def abrir_periodo(self):
        if self.estado == "Abierto":
            return "⚠️ El periodo ya está abierto."
        else:
            self.estado = "Abierto"
            return "✅ El periodo ha sido abierto correctamente."

    def cerrar_periodo(self):
        if self.estado == "Cerrado":
            return "⚠️ El periodo ya está cerrado."
        else:
            self.estado = "Cerrado"
            return "✅ El periodo ha sido cerrado correctamente."


# --- Ventana principal ---
root = tk.Tk()
root.title("Sistema de Asignación de Cupo")
root.geometry("900x650")
root.config(bg="#cfe8ef")

# Ruta del logo
ruta_logo = os.path.join(os.path.dirname(__file__), "..", "imagenes", "SAC-LOGO.png")
ruta_logo = os.path.abspath(ruta_logo)

# Cargar logo
logo = Image.open(ruta_logo).convert("RGBA")
logo = logo.resize((130, 130), Image.Resampling.LANCZOS)
logo_tk = ImageTk.PhotoImage(logo)

lbl_logo = tk.Label(root, image=logo_tk, bg="#cfe8ef")
lbl_logo.place(relx=0.03, rely=0.05, anchor="nw")

# Marco tipo tarjeta
card = tk.Frame(root, bg="#e2f1f8", highlightthickness=2,
                highlightbackground="#1b3b6f", padx=40, pady=40)
card.place(relx=0.5, rely=0.5, anchor="center")

# Título y subtítulo
tk.Label(card, text="Sistema de Asignación de Cupo",
         font=("Segoe UI", 22, "bold"), fg="#1b3b6f", bg="#e2f1f8").pack(pady=(0, 20))

tk.Label(card, text="Seleccione una opción para continuar",
         font=("Segoe UI", 12), fg="#2f2f2f", bg="#e2f1f8").pack(pady=(0, 25))


# --- Función para crear botones ---
def crear_boton(texto, color="#1b3b6f", hover="#2b4f8a", comando=None):
    boton = tk.Button(card,
                      text=texto,
                      font=("Segoe UI Semibold", 13),
                      fg="white",
                      bg=color,
                      activebackground=hover,
                      activeforeground="white",
                      relief="flat",
                      cursor="hand2",
                      height=2,
                      width=25,
                      command=comando)
    boton.pack(pady=8, fill="x")
    return boton


# --- Funcionalidad de Crear nuevo periodo ---
def abrir_ventana_periodo():
    ventana = tk.Toplevel(root)
    ventana.title("Nuevo Período Académico")
    ventana.geometry("400x400")
    ventana.config(bg="#e2f1f8")

    tk.Label(ventana, text="Crear nuevo período académico",
             font=("Segoe UI", 14, "bold"), bg="#e2f1f8", fg="#1b3b6f").pack(pady=10)

    # Entradas
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

    # Crear objeto Periodo
    def crear_periodo():
        try:
            codigo = entry_codigo.get()
            fecha_inicio = datetime.strptime(entry_inicio.get(), "%d/%m/%Y")
            fecha_fin = datetime.strptime(entry_fin.get(), "%d/%m/%Y")

            if fecha_fin < fecha_inicio:
                messagebox.showwarning("Error", "La fecha de fin no puede ser anterior a la de inicio.")
                return

            estado = entry_estado.get().capitalize()
            if estado not in ["Abierto", "Cerrado"]:
                messagebox.showwarning("Error", "Estado no válido. Use Abierto o Cerrado.")
                return

            global periodo_actual
            periodo_actual = PeriodoAcademico(codigo, fecha_inicio, fecha_fin, estado)

            messagebox.showinfo("Éxito", "Período académico creado correctamente.")
            ventana.destroy()

            mostrar_periodo()
        except ValueError:
            messagebox.showwarning("Error", "Formato de fecha inválido. Use dd/mm/aaaa.")

    tk.Button(ventana, text="Crear Período", bg="#1b3b6f", fg="white",
              relief="flat", width=20, command=crear_periodo).pack(pady=20)


# --- Mostrar información del período ---
def mostrar_periodo():
    if 'periodo_actual' not in globals():
        messagebox.showwarning("Aviso", "No hay ningún período creado.")
        return

    ventana_info = tk.Toplevel(root)
    ventana_info.title("Información del Período")
    ventana_info.geometry("400x350")
    ventana_info.config(bg="#e2f1f8")

    p = periodo_actual

    tk.Label(ventana_info, text="Información del período académico",
             font=("Segoe UI", 14, "bold"), bg="#e2f1f8", fg="#1b3b6f").pack(pady=10)

    info = (
        f"Código: {p.codigo}\n"
        f"Fecha de inicio: {p.fecha_inicio.strftime('%d/%m/%Y')}\n"
        f"Fecha de fin: {p.fecha_fin.strftime('%d/%m/%Y')}\n"
        f"Estado actual: {p.estado}"
    )

    lbl_info = tk.Label(ventana_info, text=info, bg="#e2f1f8", justify="left")
    lbl_info.pack(pady=10)

    # Botones para abrir/cerrar
    def abrir_periodo():
        msg = p.abrir_periodo()
        messagebox.showinfo("Estado", msg)
        lbl_info.config(text=(
            f"Código: {p.codigo}\n"
            f"Fecha de inicio: {p.fecha_inicio.strftime('%d/%m/%Y')}\n"
            f"Fecha de fin: {p.fecha_fin.strftime('%d/%m/%Y')}\n"
            f"Estado actual: {p.estado}"
        ))

    def cerrar_periodo():
        msg = p.cerrar_periodo()
        messagebox.showinfo("Estado", msg)
        lbl_info.config(text=(
            f"Código: {p.codigo}\n"
            f"Fecha de inicio: {p.fecha_inicio.strftime('%d/%m/%Y')}\n"
            f"Fecha de fin: {p.fecha_fin.strftime('%d/%m/%Y')}\n"
            f"Estado actual: {p.estado}"
        ))

    tk.Button(ventana_info, text="Abrir Período", bg="#1b3b6f", fg="white",
              relief="flat", width=15, command=abrir_periodo).pack(pady=5)

    tk.Button(ventana_info, text="Cerrar Período", bg="#d9534f", fg="white",
              relief="flat", width=15, command=cerrar_periodo).pack(pady=5)


# --- Botones principales ---
crear_boton("Crear nuevo período", comando=abrir_ventana_periodo)
crear_boton("Ver información de período", comando=mostrar_periodo)
crear_boton("Configurar carrera")
crear_boton("Cargar archivo")
crear_boton("Ver resultados")
crear_boton("Exportar resultados")

# Botón Salir
tk.Button(card, text="Salir", font=("Segoe UI Semibold", 13),
          fg="white", bg="#d9534f", activebackground="#c9302c",
          relief="flat", cursor="hand2", height=2, width=25,
          command=root.destroy).pack(pady=20, fill="x")

# Pie de página
footer = tk.Label(root, text="© 2025 Sistema Académico - SAC",
                  font=("Segoe UI", 9), fg="#1b3b6f", bg="#cfe8ef")
footer.pack(side="bottom", pady=10)

root.mainloop()
