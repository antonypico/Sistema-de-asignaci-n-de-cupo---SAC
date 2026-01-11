import tkinter as tk
from tkinter import ttk, filedialog, messagebox


class FormCargarArchivo(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("Cargar Archivo")
        self.geometry("480x260")
        self.resizable(False, False)
        self._centrar_ventana()

        self.ruta_archivo = tk.StringVar()
        self._crear_widgets()

    def _centrar_ventana(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 240
        y = (self.winfo_screenheight() // 2) - 130
        self.geometry(f"+{x}+{y}")

    def _crear_widgets(self):
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(
            frame,
            text="Carga de Archivos",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=10)

        fila = ttk.Frame(frame)
        fila.pack(fill="x", pady=10)

        ttk.Entry(
            fila,
            textvariable=self.ruta_archivo,
            state="readonly"
        ).pack(side="left", fill="x", expand=True, padx=5)

        ttk.Button(
            fila,
            text="Buscar",
            command=self._buscar_archivo
        ).pack(side="right")

        botones = ttk.Frame(frame)
        botones.pack(pady=20)

        ttk.Button(botones, text="Cargar", command=self._cargar).grid(row=0, column=0, padx=5)
        ttk.Button(botones, text="Cerrar", command=self.destroy).grid(row=0, column=1, padx=5)

    def _buscar_archivo(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo",
            filetypes=[("Archivos Excel", "*.xlsx"), ("Todos", "*.*")]
        )
        if ruta:
            self.ruta_archivo.set(ruta)

    def _cargar(self):
        if not self.ruta_archivo.get():
            messagebox.showwarning("Advertencia", "Seleccione un archivo")
            return
        messagebox.showinfo("Éxito", "Archivo cargado correctamente (simulado)")


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    FormCargarArchivo(root)
    root.mainloop()
