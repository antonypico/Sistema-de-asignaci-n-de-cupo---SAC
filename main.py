import tkinter as tk
from forms.form_login import VentanaLogin

if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaLogin(root)
    root.mainloop()
    