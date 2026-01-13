class Estudiante:
    def __init__(
        self,
        id_postulante,
        correo,
        num_telefono,
        nombres,
        apellidos,
        nota_postulacion,
        opcion_1,
        politica_cuotas=False,
        vulnerable=False,
        cuadro_honor=False,
        pueblo_nacionalidad=False,
        titulo_superior=False,
        otro_merito=False
    ):
        # IDENTIFICACIÓN
        self.id_postulante = id_postulante
        self.correo = correo
        self.num_telefono = num_telefono
        self.nombres = nombres
        self.apellidos = apellidos

        # MÉRITO ACADÉMICO
        self.nota_postulacion = float(nota_postulacion)

        # OPCIONES DE CARRERA
        self.opciones_carrera = [opcion_1]

        # SEGMENTOS / PRIORIDADES
        self.es_politica_cuotas = bool(politica_cuotas)
        self.es_vulnerable = bool(vulnerable)
        self.es_cuadro_honor = bool(cuadro_honor)
        self.es_pueblo_nacionalidad = bool(pueblo_nacionalidad)
        self.tiene_titulo_superior = bool(titulo_superior)
        self.tiene_otro_merito = bool(otro_merito)

        # RESULTADO DE ASIGNACIÓN
        self.oferta_asignada = None

    # -------------------------
    # ESTADO DE ASIGNACIÓN
    # -------------------------

    def esta_asignado(self):
        return self.oferta_asignada is not None

    def marcar_asignado(self, oferta):
        self.oferta_asignada = oferta

    # -------------------------
    # CONSULTAS ÚTILES
    # -------------------------

    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"

    def carrera_postulada(self):
        """Retorna la primera opción de carrera"""
        return self.opciones_carrera[0]

    # -------------------------
    # PERSISTENCIA
    # -------------------------

    def a_diccionario(self):
        return {
            "id_postulante": self.id_postulante,
            "correo": self.correo,
            "num_telefono": self.num_telefono,
            "nombres": self.nombres,
            "apellidos": self.apellidos,
            "nota_postulacion": self.nota_postulacion,
            "opcion_1": self.opciones_carrera[0],
            "politica_cuotas": self.es_politica_cuotas,
            "vulnerable": self.es_vulnerable,
            "cuadro_honor": self.es_cuadro_honor,
            "pueblo_nacionalidad": self.es_pueblo_nacionalidad,
            "titulo_superior": self.tiene_titulo_superior,
            "otro_merito": self.tiene_otro_merito
        }

    @staticmethod
    def desde_diccionario(data):
        return Estudiante(
            id_postulante=data["id_postulante"],
            correo=data["correo"],
            num_telefono=data["num_telefono"],
            nombres=data["nombres"],
            apellidos=data["apellidos"],
            nota_postulacion=data["nota_postulacion"],
            opcion_1=data["opcion_1"],
            politica_cuotas=data.get("politica_cuotas", False),
            vulnerable=data.get("vulnerable", False),
            cuadro_honor=data.get("cuadro_honor", False),
            pueblo_nacionalidad=data.get("pueblo_nacionalidad", False),
            titulo_superior=data.get("titulo_superior", False),
            otro_merito=data.get("otro_merito", False)
        )