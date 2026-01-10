from domain.carrera import Carrera
from domain.oferta_academica import OfertaAcademica

# Carreras
carrera_sistemas = Carrera(
    nombre="Ingenieria en Sistemas",
    area="Ingenieria",
    subarea="Software",
    nivel="Tercer Nivel",
    modalidad="Presencial",
    jornada="Matutina",
    institucion="ULEAM"
)

carrera_administracion = Carrera(
    nombre="Administracion de Empresas",
    area="Administracion",
    subarea="Empresas",
    nivel="Tercer Nivel",
    modalidad="Presencial",
    jornada="Vespertina",
    institucion="ULEAM"
)

# Ofertas (cupos pequeños para forzar reglas)
ofertas = [
    OfertaAcademica(carrera_sistemas, total_cupos=3),
    OfertaAcademica(carrera_administracion, total_cupos=20)
]
