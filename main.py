import tkinter as tk
from iu.login.form_login import LoginView


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Oculta ventana raíz
    LoginView(root)
    root.mainloop()
