import tkinter as tk
from tkinter import ttk, messagebox

class FormExportarResultados(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Exportar Resultados")
        self.geometry("400x250")
        self.resizable(False, False)

        self.crear_widgets()

    def crear_widgets(self):
        # Título
        lbl_titulo = tk.Label(
            self,
            text="Exportar Resultados",
            font=("Arial", 14, "bold")
        )
        lbl_titulo.pack(pady=15)

        # Selección de formato
        frame = tk.Frame(self)
        frame.pack(pady=10)

        tk.Label(frame, text="Formato de exportación:").grid(row=0, column=0, padx=5)

        self.formato = ttk.Combobox(
            frame,
            values=["PDF", "Excel", "CSV"],
            state="readonly"
        )
        self.formato.current(0)
        self.formato.grid(row=0, column=1, padx=5)

        # Botón exportar
        btn_exportar = tk.Button(
            self,
            text="Exportar",
            width=15,
            command=self.exportar
        )
        btn_exportar.pack(pady=15)

        # Botón cancelar
        btn_cancelar = tk.Button(
            self,
            text="Cancelar",
            width=15,
            command=self.destroy
        )
        btn_cancelar.pack()

    def exportar(self):
        formato_seleccionado = self.formato.get()
        messagebox.showinfo(
            "Exportación",
            f"Resultados exportados correctamente en formato {formato_seleccionado}"
        )


# Prueba independiente
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    FormExportarResultados(root)
    root.mainloop()
