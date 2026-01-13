import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from iu.base.ventana_base import VentanaBase


class CargarArchivoView(VentanaBase):
    def __init__(self, master=None):
        super().__init__(
            master,
            titulo="Cargar Archivo",
            ancho=500,
            alto=300
        )

        self.ruta_archivo = None
        self._crear_widgets()

    def _crear_widgets(self):
        contenedor = ttk.Frame(self)
        contenedor.pack(expand=True, padx=20, pady=20)

        ttk.Label(
            contenedor,
            text="Cargar archivo de postulantes",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        frame_archivo = ttk.Frame(contenedor)
        frame_archivo.pack(fill="x", pady=10)

        self.entry_ruta = ttk.Entry(frame_archivo)
        self.entry_ruta.pack(side="left", fill="x", expand=True, padx=(0, 10))

        ttk.Button(
            frame_archivo,
            text="Buscar...",
            command=self._buscar_archivo
        ).pack(side="right")

        frame_botones = ttk.Frame(contenedor)
        frame_botones.pack(pady=25)

        ttk.Button(
            frame_botones,
            text="Cargar",
            command=self._cargar_archivo
        ).pack(side="left", padx=10)

        ttk.Button(
            frame_botones,
            text="Cancelar",
            command=self.destroy
        ).pack(side="left", padx=10)

    def _buscar_archivo(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo",
            filetypes=[
                ("Archivos Excel", "*.xlsx *.xls"),
                ("Todos los archivos", "*.*")
            ]
        )

        if ruta:
            self.ruta_archivo = ruta
            self.entry_ruta.delete(0, tk.END)
            self.entry_ruta.insert(0, ruta)

    def _cargar_archivo(self):
        if not self.ruta_archivo:
            messagebox.showwarning(
                "Advertencia",
                "Debe seleccionar un archivo primero"
            )
            return

        # Aquí luego se conectará con la lectura real del Excel
        messagebox.showinfo(
            "Éxito",
            "Archivo cargado correctamente"
        )

        self.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    CargarArchivoView(root)
    root.mainloop()
