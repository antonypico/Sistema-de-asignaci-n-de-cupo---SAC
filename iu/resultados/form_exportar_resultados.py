import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from iu.base.ventana_base import VentanaBase


class ExportarResultadosView(VentanaBase):
    def __init__(self, master=None):
        super().__init__(
            master,
            titulo="Exportar Resultados",
            ancho=500,
            alto=300
        )

        self.ruta_destino = None
        self._crear_widgets()

    def _crear_widgets(self):
        contenedor = ttk.Frame(self)
        contenedor.pack(expand=True, padx=20, pady=20)

        ttk.Label(
            contenedor,
            text="Exportar resultados de asignación",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        frame_ruta = ttk.Frame(contenedor)
        frame_ruta.pack(fill="x", pady=10)

        self.entry_ruta = ttk.Entry(frame_ruta)
        self.entry_ruta.pack(side="left", fill="x", expand=True, padx=(0, 10))

        ttk.Button(
            frame_ruta,
            text="Seleccionar...",
            command=self._seleccionar_ruta
        ).pack(side="right")

        frame_botones = ttk.Frame(contenedor)
        frame_botones.pack(pady=25)

        ttk.Button(
            frame_botones,
            text="Exportar",
            command=self._exportar
        ).pack(side="left", padx=10)

        ttk.Button(
            frame_botones,
            text="Cancelar",
            command=self.destroy
        ).pack(side="left", padx=10)

    def _seleccionar_ruta(self):
        ruta = filedialog.asksaveasfilename(
            title="Guardar archivo",
            defaultextension=".xlsx",
            filetypes=[
                ("Archivo Excel", "*.xlsx"),
                ("Todos los archivos", "*.*")
            ]
        )

        if ruta:
            self.ruta_destino = ruta
            self.entry_ruta.delete(0, tk.END)
            self.entry_ruta.insert(0, ruta)

    def _exportar(self):
        if not self.ruta_destino:
            messagebox.showwarning(
                "Advertencia",
                "Debe seleccionar una ruta para exportar"
            )
            return

        # Aquí luego se conectará con la generación real del Excel
        messagebox.showinfo(
            "Éxito",
            "Resultados exportados correctamente"
        )

        self.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    ExportarResultadosView(root)
    root.mainloop()
