import tkinter as tk
from tkinter import ttk, messagebox


class FormConfigurarCarrera(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("Configurar Carrera")
        self.geometry("500x420")
        self.resizable(False, False)
        self._centrar_ventana()

        self._crear_widgets()

    def _centrar_ventana(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 250
        y = (self.winfo_screenheight() // 2) - 210
        self.geometry(f"+{x}+{y}")

    def _crear_widgets(self):
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(
            frame,
            text="Configuración de Carrera",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=10)

        self.campos = []

        self._campo(frame, "Nombre de la carrera:")
        self._campo(frame, "Área:")
        self._campo(frame, "Modalidad:")
        self._campo(frame, "Jornada:")
        self._campo(frame, "Cupos Nivelación:")
        self._campo(frame, "Cupos Primer Semestre:")

        botones = ttk.Frame(frame)
        botones.pack(pady=20)

        ttk.Button(botones, text="Guardar", command=self._guardar).grid(row=0, column=0, padx=5)
        ttk.Button(botones, text="Limpiar", command=self._limpiar).grid(row=0, column=1, padx=5)
        ttk.Button(botones, text="Cerrar", command=self.destroy).grid(row=0, column=2, padx=5)

    def _campo(self, parent, texto):
        fila = ttk.Frame(parent)
        fila.pack(fill="x", pady=5)

        ttk.Label(fila, text=texto, width=25).pack(side="left")

        entrada = ttk.Entry(fila)
        entrada.pack(side="right", fill="x", expand=True)
        self.campos.append(entrada)

    def _guardar(self):
        messagebox.showinfo("Guardar", "Carrera guardada correctamente (simulado)")

    def _limpiar(self):
        for entrada in self.campos:
            entrada.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    FormConfigurarCarrera(root)
    root.mainloop()
