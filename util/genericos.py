from PIL import ImageTk , Image 

def leer_imagen(path, size):
    return ImageTk.PhotoImage(Image.open(path).resize(size, Image.Resampling.LANCZOS))

def centrar_ventana(root, ancho, alto):
    pantalla_ancho = root.winfo_screenwidth()
    pantalla_alto = root.winfo_screenheight()
    x = int((pantalla_ancho - ancho) / 2)
    y = int((pantalla_alto - alto) / 2)

    root.geometry(f"{ancho}x{alto}+{x}+{y}")

