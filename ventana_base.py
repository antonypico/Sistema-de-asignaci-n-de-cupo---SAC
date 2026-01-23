import tkinter as tk
from tkinter import ttk, messagebox
from iu.base.ventana_base import VentanaBase # type: ignore


class PeriodosAcademicosView(VentanaBase):
    def __init__(self, master=None):
        super().__init__(
            master,
            titulo="Gestión de Períodos Académicos - SAC",
            ancho=550,
            alto=450
        )

        self.periodos = []  # Simula la lista de períodos (lógica simple)
        self._crear_widgets()

    def _crear_widgets(self):
        contenedor = ttk.Frame(self, padding=20)
        contenedor.pack(expand=True, fill="both")

        ttk.Label(
            contenedor,
            text="Períodos Académicos",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        # Formulario
        form = ttk.Frame(contenedor)
        form.pack(fill="x", pady=10)

        ttk.Label(form, text="Nombre del período").grid(row=0, column=0, sticky="w")
        self.entry_periodo = ttk.Entry(form, width=30)
        self.entry_periodo.grid(row=1, column=0, padx=5, pady=5)

        ttk.Button(
            form,
            text="Agregar Período",
            command=self.agregar_periodo
        ).grid(row=1, column=1, padx=10)

        # Lista de períodos
        ttk.Label(contenedor, text="Listado de períodos").pack(anchor="w", pady=10)

        self.lista_periodos = tk.Listbox(contenedor, height=8)
        self.lista_periodos.pack(fill="both", expand=True)

    def agregar_periodo(self):
        periodo = self.entry_periodo.get().strip()

        if not periodo:
            messagebox.showwarning("Advertencia", "Ingrese un nombre de período")
            return

        self.periodos.append(periodo)
        self.lista_periodos.insert(tk.END, periodo)
        self.entry_periodo.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    PeriodosAcademicosView(root)
    root.mainloop()
