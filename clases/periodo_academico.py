from datetime import datetime
import json
import os


class PeriodoAcademico:
    ARCHIVO_JSON = os.path.join(os.path.dirname(__file__), "..", "data", "periodos.json")

    def __init__(self, codigo, fecha_inicio, fecha_fin, estado):
        self.codigo = codigo
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.estado = estado

    @staticmethod
    def validar_fechas(fecha_inicio, fecha_fin):
        """Valida formato y orden de fechas."""
        try:
            inicio = datetime.strptime(fecha_inicio, "%d/%m/%Y")
            fin = datetime.strptime(fecha_fin, "%d/%m/%Y")
            if fin < inicio:
                return None, None, " La fecha de fin no puede ser anterior a la de inicio."
            return inicio, fin, None
        except ValueError:
            return None, None, " Formato inválido. Use dd/mm/aaaa."

    @staticmethod
    def validar_estado(estado):
        """Valida que el estado sea correcto."""
        estado = estado.capitalize()
        if estado not in ["Abierto", "Cerrado"]:
            return None, " Estado no válido. Use 'Abierto' o 'Cerrado'."
        return estado, None

    def abrir_periodo(self):
        if self.estado == "Abierto":
            return " El período ya está abierto."
        self.estado = "Abierto"
        return "El período ha sido abierto correctamente."

    def cerrar_periodo(self):
        if self.estado == "Cerrado":
            return " El período ya está cerrado."
        self.estado = "Cerrado"
        return " El período ha sido cerrado correctamente."

    def to_dict(self):
        """Convierte el objeto en un diccionario para guardar en JSON."""
        return {
            "codigo": self.codigo,
            "fecha_inicio": self.fecha_inicio.strftime("%d/%m/%Y"),
            "fecha_fin": self.fecha_fin.strftime("%d/%m/%Y"),
            "estado": self.estado
        }

    @classmethod
    def guardar(cls, lista_periodos):
        """Guarda la lista de períodos en un archivo JSON."""
        os.makedirs(os.path.dirname(cls.ARCHIVO_JSON), exist_ok=True)
        data = [p.to_dict() for p in lista_periodos]
        with open(cls.ARCHIVO_JSON, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    @classmethod
    def cargar(cls):
        """Carga la lista de períodos desde el archivo JSON."""
        if not os.path.exists(cls.ARCHIVO_JSON):
            return []
        with open(cls.ARCHIVO_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
            periodos = []
            for d in data:
                inicio = datetime.strptime(d["fecha_inicio"], "%d/%m/%Y")
                fin = datetime.strptime(d["fecha_fin"], "%d/%m/%Y")
                p = PeriodoAcademico(d["codigo"], inicio, fin, d["estado"])
                periodos.append(p)
            return periodos

