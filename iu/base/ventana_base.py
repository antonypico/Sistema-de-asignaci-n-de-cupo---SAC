import tkinter as tk


class VentanaBase(tk.Toplevel):
    def __init__(self, master=None, titulo="Sistema Académico", ancho=900, alto=600):
        super().__init__(master)

        self.title(titulo)
        self.ancho = ancho
        self.alto = alto

        self._configurar_ventana()
        self._centrar_ventana()

    def _configurar_ventana(self):
        self.geometry(f"{self.ancho}x{self.alto}")
        self.resizable(False, False)
        self.configure(bg="#E6F2F8")  

    def _centrar_ventana(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.ancho // 2)
        y = (self.winfo_screenheight() // 2) - (self.alto // 2)
        self.geometry(f"{self.ancho}x{self.alto}+{x}+{y}")


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    VentanaBase(root, "Prueba Ventana Base")
    root.mainloop()
