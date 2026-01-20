"""
Script de prueba para validar la corrección del problema de cupos
Simula: 1000 cupos disponibles, 2000 postulantes cargados
Resultado esperado: 1000 asignados, 1000 no asignados
"""

import json
import os
from datetime import datetime
from domain.estudiante import Estudiante
from domain.oferta_academica import OfertaAcademica
from services.asignacion_service import AsignacionService
from services.postulante_service import PostulanteService
from services.oferta_academica_service import OfertaAcademicaService
from services.periodo_service import PeriodoService
from services.desempate_service import DesempateService

def crear_datos_prueba():
    """Crea datos de prueba: 1000 cupos, 2000 postulantes"""
    
    print("\n=== CREANDO DATOS DE PRUEBA ===\n")
    
    # Crear período
    periodo_service = PeriodoService()
    periodo_activo = periodo_service.obtener_periodo_activo()
    
    if not periodo_activo:
        print("ERROR: No existe período activo")
        return False
    
    ruta = periodo_service.obtener_ruta_periodo_activo()
    print(f"Período activo: {periodo_activo}")
    print(f"Ruta: {ruta}\n")
    
    # Crear ofertas: 5 carreras x 200 cupos = 1000 cupos totales
    ofertas = []
    carreras = [
        ("ING001", "Ingeniería en Sistemas", 200),
        ("ING002", "Ingeniería Industrial", 200),
        ("ADM001", "Administración de Empresas", 200),
        ("CON001", "Contabilidad", 200),
        ("DER001", "Derecho", 200)
    ]
    
    for codigo, nombre, cupos in carreras:
        oferta = OfertaAcademica(
            codigo_carrera=codigo,
            institucion="Universidad Prueba",
            provincia="Pichincha",
            canton="Quito",
            nombre_carrera=nombre,
            area="Ingeniería",
            nivel="Pregrado",
            modalidad="Presencial",
            jornada="Diurna",
            tipo_cupo="Regular",
            total_cupos=cupos,
            periodo="2025-2"
        )
        ofertas.append(oferta)
        print(f"Carrera: {nombre} - {cupos} cupos")
    
    # Guardar ofertas
    oferta_service = OfertaAcademicaService()
    oferta_service.guardar_ofertas(ofertas)
    print(f"\nOfertas guardadas: {len(ofertas)}\n")
    
    # Crear 2000 postulantes con múltiples opciones
    postulantes = []
    codigos_carreras = ["ING001", "ING002", "ADM001", "CON001", "DER001"]
    
    for i in range(2000):
        # Cada estudiante tiene opciones diferentes para distribuirse
        # Usar rotación para distribuir entre opciones
        opcion_1 = codigos_carreras[i % 5]
        opcion_2 = codigos_carreras[(i + 1) % 5]
        opcion_3 = codigos_carreras[(i + 2) % 5]
        
        estudiante = Estudiante(
            id_postulante=f"EST{i+1:05d}",
            nombres=f"Estudiante{i+1}",
            apellidos=f"Prueba{i+1}",
            correo=f"est{i+1}@test.com",
            num_telefono="0999999999",
            nota_postulacion=80.0 + (i % 20),  # Notas entre 80 y 100
            opcion_1=opcion_1
        )
        # Agregar opciones adicionales
        estudiante.opciones_carrera.append(opcion_2)
        estudiante.opciones_carrera.append(opcion_3)
        
        postulantes.append(estudiante)
    
    # Guardar postulantes
    postulante_service = PostulanteService()
    postulante_service.guardar_postulantes(postulantes)
    print(f"Postulantes cargados: {len(postulantes)}\n")
    
    print("\n" + "=" * 50)
    print(f"ESTADO INICIAL:")
    print(f"  Cupos totales: 1000")
    print(f"  Postulantes: 2000")
    print(f"  Esperado: 1000 asignados, 1000 no asignados")
    print("=" * 50 + "\n")
    
    return True

def ejecutar_prueba():
    """Ejecuta la asignación y valida los resultados"""
    
    print("\n=== EJECUTANDO ASIGNACIÓN ===\n")
    
    asignacion_service = AsignacionService()
    
    # Diagnóstico antes
    print("DIAGNÓSTICO PRE-ASIGNACIÓN:")
    asignacion_service.diagnosticar_ofertas()
    
    try:
        # Ejecutar asignación
        print("Iniciando proceso de asignación...\n")
        asignacion_service.ejecutar_asignacion()
        print("\nAsignación completada\n")
        
    except Exception as e:
        print(f"ERROR durante asignación: {e}")
        return False
    
    # Diagnóstico después
    print("DIAGNÓSTICO POST-ASIGNACIÓN:")
    asignacion_service.diagnosticar_ofertas()
    
    # Validar resultados
    print("\n=== VALIDACIÓN DE RESULTADOS ===\n")
    
    periodo_service = PeriodoService()
    ruta = periodo_service.obtener_ruta_periodo_activo()
    archivo_resultados = f"{ruta}/resultados_asignacion.json"
    
    if not os.path.exists(archivo_resultados):
        print("ERROR: Archivo de resultados no encontrado")
        return False
    
    with open(archivo_resultados, 'r', encoding='utf-8') as f:
        resultados = json.load(f)
    
    asignados = sum(1 for r in resultados if r['estado_asignacion'] == 'ASIGNADO')
    no_asignados = sum(1 for r in resultados if r['estado_asignacion'] == 'NO ASIGNADO')
    
    print(f"Total resultados: {len(resultados)}")
    print(f"Asignados: {asignados}")
    print(f"No asignados: {no_asignados}\n")
    
    # Validar por carrera
    print("Distribución por carrera:")
    by_carrera = {}
    for r in resultados:
        if r['estado_asignacion'] == 'ASIGNADO':
            carrera = r['carrera']
            by_carrera[carrera] = by_carrera.get(carrera, 0) + 1
    
    for carrera, count in sorted(by_carrera.items()):
        print(f"  {carrera}: {count}")
    
    print("\n" + "=" * 50)
    
    # Verificar si pasó la prueba
    if asignados == 1000 and no_asignados == 1000:
        print("EXITO: Exactamente 1000 asignados")
        return True
    else:
        print(f"FALLO: Se esperaba 1000 asignados, se obtuvieron {asignados}")
        return False

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  TEST DE CORRECCION DE CUPOS - Sistema de Asignacion SAC")
    print("=" * 60)
    
    # Crear datos de prueba
    if not crear_datos_prueba():
        print("No se pudieron crear los datos de prueba")
        exit(1)
    
    # Ejecutar prueba
    if ejecutar_prueba():
        print("\nLa correccin de cupos funciona correctamente!")
    else:
        print("\nAun hay problemas con la asignacin de cupos")
