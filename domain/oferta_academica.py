class Carrera:
    """
    Objeto simple para compatibilidad con los Strategy
    """
    def __init__(self, nombre):
        self.nombre = nombre


class OfertaAcademica:
    def __init__(
        self,
        codigo_carrera,
        institucion,
        provincia,
        canton,
        nombre_carrera,
        area,
        nivel,
        modalidad,
        jornada,
        tipo_cupo,
        total_cupos,
        periodo
    ):
        self.codigo_carrera = codigo_carrera
        self.institucion = institucion
        self.provincia = provincia
        self.canton = canton
        self.nombre_carrera = nombre_carrera
        self.area = area
        self.nivel = nivel
        self.modalidad = modalidad
        self.jornada = jornada
        self.tipo_cupo = tipo_cupo
        self.total_cupos = total_cupos
        self.cupos_disponibles = total_cupos
        self.periodo = periodo

        # 🔑 ADAPTADOR PARA LOS STRATEGY
        self.carrera = Carrera(nombre_carrera)

    # -------------------------
    # LÓGICA DE CUPOS
    # -------------------------

    def tiene_cupos(self):
        return self.cupos_disponibles > 0

    def consumir_cupo(self):
        if self.cupos_disponibles > 0:
            self.cupos_disponibles -= 1

    # -------------------------
    # PERSISTENCIA
    # -------------------------

    def a_diccionario(self):
        return {
            "codigo_carrera": self.codigo_carrera,
            "institucion": self.institucion,
            "provincia": self.provincia,
            "canton": self.canton,
            "nombre_carrera": self.nombre_carrera,
            "area": self.area,
            "nivel": self.nivel,
            "modalidad": self.modalidad,
            "jornada": self.jornada,
            "tipo_cupo": self.tipo_cupo,
            "total_cupos": self.total_cupos,
            "cupos_disponibles": self.cupos_disponibles,
            "periodo": self.periodo
        }

    @staticmethod
    def desde_diccionario(data):
        oferta = OfertaAcademica(
            codigo_carrera=data["codigo_carrera"],
            institucion=data["institucion"],
            provincia=data["provincia"],
            canton=data["canton"],
            nombre_carrera=data["nombre_carrera"],
            area=data["area"],
            nivel=data["nivel"],
            modalidad=data["modalidad"],
            jornada=data["jornada"],
            tipo_cupo=data["tipo_cupo"],
            total_cupos=data["total_cupos"],
            periodo=data["periodo"]
        )
        oferta.cupos_disponibles = data.get(
            "cupos_disponibles",
            data["total_cupos"]
        )
        return oferta
