# tests/ejecutar_prueba.py

from services.asignador_cupos import AsignadorCupos
from tests.datos_estudiantes_prueba import estudiantes
from tests.datos_oferta_prueba import ofertas

asignador = AsignadorCupos(estudiantes, ofertas)
resultados = asignador.ejecutar()

print("RESULTADOS FINALES")
print("------------------")
for r in resultados:
    print(f"{r.id_estudiante} | {r.nombre} | {r.carrera_asignada}")