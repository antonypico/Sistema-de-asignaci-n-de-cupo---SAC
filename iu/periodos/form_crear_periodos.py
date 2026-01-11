import tkinter as tk
from tkinter import messagebox


class CrearPeriodo(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Crear Período Académico")
        self.ancho = 500
        self.alto = 350

        self._configurar_ventana()
        self._centrar_ventana()
        self._crear_widgets()

    def _configurar_ventana(self):
        self.geometry(f"{self.ancho}x{self.alto}")
        self.resizable(False, False)
        self.configure(bg="#E6F2F8")

    def _centrar_ventana(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.ancho // 2)
        y = (self.winfo_screenheight() // 2) - (self.alto // 2)
        self.geometry(f"{self.ancho}x{self.alto}+{x}+{y}")

    def _crear_widgets(self):
        tk.Label(
            self,
            text="CREAR PERÍODO ACADÉMICO",
            font=("Arial", 14, "bold"),
            bg="#E6F2F8"
        ).pack(pady=15)

        frame = tk.Frame(self, bg="#E6F2F8")
        frame.pack(pady=10)

        tk.Label(frame, text="Nombre del período:", bg="#E6F2F8").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_nombre = tk.Entry(frame, width=30)
        self.entry_nombre.grid(row=0, column=1)

        tk.Label(frame, text="Fecha inicio:", bg="#E6F2F8").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_inicio = tk.Entry(frame, width=30)
        self.entry_inicio.grid(row=1, column=1)

        tk.Label(frame, text="Fecha fin:", bg="#E6F2F8").grid(row=2, column=0, sticky="w", pady=5)
        self.entry_fin = tk.Entry(frame, width=30)
        self.entry_fin.grid(row=2, column=1)

        tk.Button(
            self,
            text="Guardar Período",
            width=20,
            command=self.guardar_periodo
        ).pack(pady=20)

    def guardar_periodo(self):
        nombre = self.entry_nombre.get()
        inicio = self.entry_inicio.get()
        fin = self.entry_fin.get()

        if not nombre or not inicio or not fin:
            messagebox.showwarning("Error", "Todos los campos son obligatorios")
            return

        messagebox.showinfo(
            "Éxito",
            f"Período '{nombre}' creado correctamente"
        )

        self.entry_nombre.delete(0, tk.END)
        self.entry_inicio.delete(0, tk.END)
        self.entry_fin.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()   # oculta ventana raíz
    CrearPeriodo(root)
    root.mainloop()
