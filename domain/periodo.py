from datetime import date


class Periodo:

    def __init__(self, nombre, fecha_inicio, fecha_fin, activo=False):
        self.nombre = nombre
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.activo = activo

    def a_diccionario(self):
        return {
            "nombre": self.nombre,
            "fecha_inicio": self.fecha_inicio.isoformat(),
            "fecha_fin": self.fecha_fin.isoformat(),
            "activo": self.activo
        }

    @staticmethod
    def desde_diccionario(data):
        return Periodo(
            nombre=data["nombre"],
            fecha_inicio=date.fromisoformat(data["fecha_inicio"]),
            fecha_fin=date.fromisoformat(data["fecha_fin"]),
            activo=data.get("activo", False)
        )
