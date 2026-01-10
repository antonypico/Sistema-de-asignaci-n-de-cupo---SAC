# tests/datos_estudiantes_prueba.py

from domain.estudiante import Estudiante

estudiantes = [

    Estudiante(
        id_estudiante=1,
        nombres="Ana",
        apellidos="Cuotas",
        nota_postulacion=950,
        opciones_carrera=["Ingenieria en Sistemas", "Administracion de Empresas"],
        es_politica_cuotas=True
    ),

    Estudiante(
        id_estudiante=2,
        nombres="Luis",
        apellidos="Vulnerable",
        nota_postulacion=900,
        opciones_carrera=["Ingenieria en Sistemas"],
        es_vulnerable=True
    ),

    Estudiante(
        id_estudiante=3,
        nombres="Maria",
        apellidos="Honor",
        nota_postulacion=980,
        opciones_carrera=["Ingenieria en Sistemas"],
        es_cuadro_honor=True
    ),

    Estudiante(
        id_estudiante=4,
        nombres="Pedro",
        apellidos="Deportista",
        nota_postulacion=870,
        opciones_carrera=["Administracion de Empresas"]
    ),
]

# otros méritos
estudiantes[3].tiene_otro_merito = True

# Bachiller pueblos
estudiantes.append(
    Estudiante(
        id_estudiante=5,
        nombres="Rosa",
        apellidos="PN",
        nota_postulacion=860,
        opciones_carrera=["Ingenieria en Sistemas"],
        es_pueblo_nacionalidad=True
    )
)

# Bachiller general
estudiantes.append(
    Estudiante(
        id_estudiante=6,
        nombres="Juan",
        apellidos="Bachiller",
        nota_postulacion=840,
        opciones_carrera=["Administracion de Empresas"]
    )
)

# Población general con título previo
estudiantes.append(
    Estudiante(
        id_estudiante=7,
        nombres="Carlos",
        apellidos="TituloPrevio",
        nota_postulacion=920,
        opciones_carrera=["Ingenieria en Sistemas"],
        tiene_titulo_superior=True
    )
)

# Población general normal
estudiantes.append(
    Estudiante(
        id_estudiante=8,
        nombres="Lucia",
        apellidos="General",
        nota_postulacion=830,
        opciones_carrera=["Ingenieria en Sistemas", "Administracion de Empresas"]
    )
)
