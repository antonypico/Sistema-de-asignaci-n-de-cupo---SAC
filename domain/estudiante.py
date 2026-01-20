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
        otro_merito=False,
        fecha_nacimiento=None,
        fecha_inscripcion=None
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

        # DATOS PARA DESEMPATE
        self.fecha_nacimiento = fecha_nacimiento
        self.fecha_inscripcion = fecha_inscripcion

        # RESULTADO DE ASIGNACIÓN
        self.oferta_asignada = None
        self.observaciones = None  # Para guardar observaciones (ej: perdió desempate)
        self.perdio_desempate = False  # Marca si el estudiante perdió un desempate

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

    def obtener_segmento(self):
        """
        Determina el segmento poblacional al que pertenece el estudiante
        según el orden de precedencia del sistema
        """
        if self.es_politica_cuotas:
            return "Política de Cuotas"
        elif self.es_vulnerable:
            return "Vulnerabilidad"
        elif self.es_cuadro_honor:
            return "Mérito Académico"
        elif self.tiene_otro_merito:
            return "Otros Méritos"
        elif self.es_pueblo_nacionalidad:
            return "Bachilleres Pueblos Nacionalidades"
        else:
            return "Población General"

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
            "otro_merito": self.tiene_otro_merito,
            "fecha_nacimiento": self.fecha_nacimiento.isoformat() if self.fecha_nacimiento else None,
            "fecha_inscripcion": self.fecha_inscripcion.isoformat() if self.fecha_inscripcion else None
        }

    @staticmethod
    def desde_diccionario(data):
        from datetime import datetime
        
        # Convertir valores a booleanos correctamente
        def to_bool(val):
            if isinstance(val, bool):
                return val
            if isinstance(val, int):
                return bool(val)
            if isinstance(val, str):
                return val.lower() in ('true', '1', 'yes', 'si')
            return False
        
        # Convertir strings a datetime si existen
        def to_datetime(val):
            if val is None:
                return None
            if isinstance(val, str):
                try:
                    return datetime.fromisoformat(val)
                except:
                    return None
            return val
        
        return Estudiante(
            id_postulante=data["id_postulante"],
            correo=data["correo"],
            num_telefono=data["num_telefono"],
            nombres=data["nombres"],
            apellidos=data["apellidos"],
            nota_postulacion=data["nota_postulacion"],
            opcion_1=data["opcion_1"],
            politica_cuotas=to_bool(data.get("politica_cuotas", False)),
            vulnerable=to_bool(data.get("vulnerable", False)),
            cuadro_honor=to_bool(data.get("cuadro_honor", False)),
            pueblo_nacionalidad=to_bool(data.get("pueblo_nacionalidad", False)),
            titulo_superior=to_bool(data.get("titulo_superior", False)),
            otro_merito=to_bool(data.get("otro_merito", False)),
            fecha_nacimiento=to_datetime(data.get("fecha_nacimiento")),
            fecha_inscripcion=to_datetime(data.get("fecha_inscripcion"))
        )