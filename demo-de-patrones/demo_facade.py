from datetime import datetime
import json
import os


# CLASE REAL DEL SISTEMA
class PeriodoAcademico:
    ARCHIVO_JSON = "periodos.json"

    def __init__(self, codigo, fecha_inicio, fecha_fin, estado):
        self.codigo = codigo
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.estado = estado

    @staticmethod
    def validar_fechas(fecha_inicio, fecha_fin):
        try:
            inicio = datetime.strptime(fecha_inicio, "%d/%m/%Y")
            fin = datetime.strptime(fecha_fin, "%d/%m/%Y")
            if fin < inicio:
                return None, None, "La fecha de fin no puede ser anterior a la de inicio."
            return inicio, fin, None
        except ValueError:
            return None, None, "Formato inválido. Use dd/mm/aaaa."

    @staticmethod
    def validar_estado(estado):
        estado = estado.capitalize()
        if estado not in ["Abierto", "Cerrado"]:
            return None, "Estado no válido. Use 'Abierto' o 'Cerrado'."
        return estado, None

    def to_dict(self):
        return {
            "codigo": self.codigo,
            "fecha_inicio": self.fecha_inicio.strftime("%d/%m/%Y"),
            "fecha_fin": self.fecha_fin.strftime("%d/%m/%Y"),
            "estado": self.estado
        }

    @classmethod
    def guardar(cls, lista_periodos):
        data = [p.to_dict() for p in lista_periodos]
        with open(cls.ARCHIVO_JSON, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    @classmethod
    def cargar(cls):
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



# PATRÓN ESTRUCTURAL: FACADE

class PeriodoFacade:
    """Facade para la gestión de períodos académicos"""

    @staticmethod
    def crear_periodo(codigo, fecha_inicio, fecha_fin, estado):
        inicio, fin, error = PeriodoAcademico.validar_fechas(fecha_inicio, fecha_fin)
        if error:
            return None, error

        estado, error = PeriodoAcademico.validar_estado(estado)
        if error:
            return None, error

        return PeriodoAcademico(codigo, inicio, fin, estado), None

    @staticmethod
    def guardar_periodos(periodos):
        PeriodoAcademico.guardar(periodos)

    @staticmethod
    def cargar_periodos():
        return PeriodoAcademico.cargar()


# DEMOSTRACIÓN
if __name__ == "__main__":
    print("\nPATRÓN ESTRUCTURAL: FACADE")
    print("Gestión de Períodos Académicos")
    print("-" * 45)

    periodo, error = PeriodoFacade.crear_periodo(
        "2025A", "01/03/2025", "30/07/2025", "abierto"
    )

    if error:
        print("Error:", error)
    else:
        print("Período creado correctamente")

        PeriodoFacade.guardar_periodos([periodo])

        periodos = PeriodoFacade.cargar_periodos()
        print(f"Períodos cargados desde JSON: {len(periodos)}")
