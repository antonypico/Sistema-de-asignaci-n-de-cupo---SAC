import tkinter as tk
from tkinter import ttk


class ListarPeriodos(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Listado de Períodos Académicos")
        self.ancho = 600
        self.alto = 400

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
            text="PERÍODOS ACADÉMICOS REGISTRADOS",
            font=("Arial", 14, "bold"),
            bg="#E6F2F8"
        ).pack(pady=15)

        columnas = ("nombre", "inicio", "fin")

        self.tabla = ttk.Treeview(self, columns=columnas, show="headings")
        self.tabla.heading("nombre", text="Período")
        self.tabla.heading("inicio", text="Inicio")
        self.tabla.heading("fin", text="Fin")

        self.tabla.pack(expand=True, fill="both", padx=20, pady=10)

        # Datos de ejemplo
        datos = [
            ("2025-1", "01/04/2025", "30/08/2025"),
            ("2025-2", "01/10/2025", "28/02/2026")
        ]

        for d in datos:
            self.tabla.insert("", tk.END, values=d)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    ListarPeriodos(root)
    root.mainloop()
