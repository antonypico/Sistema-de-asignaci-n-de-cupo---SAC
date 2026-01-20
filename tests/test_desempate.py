"""
Pruebas del sistema de desempate
"""
from datetime import datetime
from domain.estudiante import Estudiante
from domain.criterio_desempate import CriterioDesempate, TipoDesempate
from services.desempate_service import DesempateService


def crear_estudiantes_prueba():
    """Crea estudiantes de prueba con la misma nota"""
    estudiantes = [
        Estudiante(
            id_postulante="P001",
            correo="juan@email.com",
            num_telefono="1234567890",
            nombres="Juan",
            apellidos="Avellaneda",
            nota_postulacion=85.5,
            opcion_1="IS1",
            fecha_nacimiento=datetime(1999, 5, 10),
            fecha_inscripcion=datetime(2024, 1, 1, 10, 0)
        ),
        Estudiante(
            id_postulante="P002",
            correo="ana@email.com",
            num_telefono="0987654321",
            nombres="Ana",
            apellidos="Benítez",
            nota_postulacion=85.5,
            opcion_1="IS1",
            fecha_nacimiento=datetime(2000, 3, 15),
            fecha_inscripcion=datetime(2024, 1, 1, 11, 0)
        ),
        Estudiante(
            id_postulante="P003",
            correo="carlos@email.com",
            num_telefono="5555555555",
            nombres="Carlos",
            apellidos="Chamorro",
            nota_postulacion=85.5,
            opcion_1="IS1",
            fecha_nacimiento=datetime(1998, 7, 20),
            fecha_inscripcion=datetime(2024, 1, 1, 9, 0)
        ),
    ]
    return estudiantes


def test_desempate_alfabetico():
    """Prueba desempate alfabético por apellido"""
    print("\n=== PRUEBA: Desempate Alfabético por Apellido ===")
    
    estudiantes = crear_estudiantes_prueba()
    criterio = CriterioDesempate("Población General", TipoDesempate.ALFABETICO_APELLIDO)
    
    ordenados = criterio.aplicar_desempate(estudiantes)
    
    print(f"Orden aplicado:")
    for i, est in enumerate(ordenados, 1):
        print(f"  {i}. {est.apellidos}, {est.nombres} (ID: {est.id_postulante})")
    
    assert ordenados[0].apellidos == "Avellaneda"
    assert ordenados[1].apellidos == "Benítez"
    assert ordenados[2].apellidos == "Chamorro"
    print("✓ Prueba exitosa")


def test_desempate_mayor_edad():
    """Prueba desempate por mayor edad"""
    print("\n=== PRUEBA: Desempate por Mayor Edad ===")
    
    estudiantes = crear_estudiantes_prueba()
    criterio = CriterioDesempate("Población General", TipoDesempate.MAYOR_EDAD)
    
    ordenados = criterio.aplicar_desempate(estudiantes)
    
    print(f"Orden aplicado (mayor edad primero):")
    for i, est in enumerate(ordenados, 1):
        print(f"  {i}. {est.nombres} {est.apellidos} - Nacido: {est.fecha_nacimiento.date()}")
    
    # Quien nació en 1998 es más viejo que quien nació en 1999 o 2000
    assert ordenados[0].id_postulante == "P003"  # 1998
    assert ordenados[1].id_postulante == "P001"  # 1999
    assert ordenados[2].id_postulante == "P002"  # 2000
    print("✓ Prueba exitosa")


def test_desempate_fecha_inscripcion():
    """Prueba desempate por fecha de inscripción"""
    print("\n=== PRUEBA: Desempate por Fecha de Inscripción ===")
    
    estudiantes = crear_estudiantes_prueba()
    criterio = CriterioDesempate("Población General", TipoDesempate.FECHA_INSCRIPCION)
    
    ordenados = criterio.aplicar_desempate(estudiantes)
    
    print(f"Orden aplicado (inscripción más temprana primero):")
    for i, est in enumerate(ordenados, 1):
        print(f"  {i}. {est.nombres} {est.apellidos} - Inscrito: {est.fecha_inscripcion}")
    
    # Quien se inscribió a las 9:00 fue primero
    assert ordenados[0].id_postulante == "P003"  # 9:00
    assert ordenados[1].id_postulante == "P001"  # 10:00
    assert ordenados[2].id_postulante == "P002"  # 11:00
    print("✓ Prueba exitosa")


def test_desempate_manual():
    """Prueba desempate manual"""
    print("\n=== PRUEBA: Desempate Manual ===")
    
    estudiantes = crear_estudiantes_prueba()
    criterio = CriterioDesempate("Población General", TipoDesempate.ALFABETICO_APELLIDO)
    
    # Establecer orden manual específico
    criterio.establecer_ordenamiento_manual(["P002", "P003", "P001"])
    
    ordenados = criterio.aplicar_desempate(estudiantes)
    
    print(f"Orden manual establecido:")
    for i, est in enumerate(ordenados, 1):
        print(f"  {i}. {est.nombres} {est.apellidos} (ID: {est.id_postulante})")
    
    assert ordenados[0].id_postulante == "P002"
    assert ordenados[1].id_postulante == "P003"
    assert ordenados[2].id_postulante == "P001"
    print("✓ Prueba exitosa")


def test_servicio_desempate():
    """Prueba el servicio completo de desempate"""
    print("\n=== PRUEBA: Servicio de Desempate ===")
    
    servicio = DesempateService()
    estudiantes = crear_estudiantes_prueba()
    
    # Obtener criterio
    criterio = servicio.obtener_criterio("Población General")
    print(f"Criterio actual para 'Población General': {criterio.tipo_desempate.value}")
    
    # Cambiar criterio
    servicio.establecer_criterio_automatico("Población General", TipoDesempate.MAYOR_EDAD)
    print(f"Criterio actualizado a: MAYOR_EDAD")
    
    # Aplicar desempate
    ordenados = servicio.aplicar_desempate("Población General", estudiantes)
    
    print(f"Estudiantes ordenados:")
    for i, est in enumerate(ordenados, 1):
        print(f"  {i}. {est.nombres} {est.apellidos}")
    
    # Agregar cambio manual
    servicio.agregar_cambio_manual("Población General", "P002", 0)
    print(f"\nCambio manual agregado: P002 en posición 0")
    
    ordenados = servicio.aplicar_desempate("Población General", estudiantes)
    print(f"Estudiantes ordenados con cambio manual:")
    for i, est in enumerate(ordenados, 1):
        print(f"  {i}. {est.nombres} {est.apellidos}")
    
    assert ordenados[0].id_postulante == "P002"
    print("✓ Prueba exitosa")


def test_persistencia():
    """Prueba guardado y carga de criterios"""
    print("\n=== PRUEBA: Persistencia de Criterios ===")
    
    # Limpiar archivo antes de la prueba
    import os
    if os.path.exists('data/criterios_desempate.json'):
        os.remove('data/criterios_desempate.json')
    
    # Crear servicio y hacer cambios
    servicio1 = DesempateService()
    servicio1.establecer_criterio_automatico("Población General", TipoDesempate.MENOR_EDAD)
    servicio1.agregar_cambio_manual("Población General", "P123", 5)
    print("Cambios realizados en servicio1")
    
    # Crear nuevo servicio (debe cargar cambios)
    servicio2 = DesempateService()
    
    # Verificar que se cargaron los cambios
    criterio = servicio2.obtener_criterio("Población General")
    print(f"Tipo cargado: {criterio.tipo_desempate}")
    assert criterio.tipo_desempate == TipoDesempate.MANUAL, f"Se esperaba MANUAL pero se obtuvo {criterio.tipo_desempate}"
    cambios = criterio.obtener_cambios_manuales()
    assert "P123" in cambios, f"P123 no encontrado en cambios manuales"
    print("✓ Cambios cargados correctamente")
    print("✓ Prueba exitosa")


def test_opciones_desempate():
    """Prueba obtención de opciones disponibles"""
    print("\n=== PRUEBA: Opciones de Desempate ===")
    
    servicio = DesempateService()
    opciones = servicio.obtener_opciones_desempate()
    
    print(f"Opciones disponibles:")
    for opcion in opciones:
        print(f"  • {opcion['etiqueta']}")
        print(f"    {opcion['descripcion']}")
    
    assert len(opciones) > 0
    print("✓ Prueba exitosa")


if __name__ == "__main__":
    print("=" * 60)
    print("PRUEBAS DEL SISTEMA DE DESEMPATE")
    print("=" * 60)
    
    try:
        test_desempate_alfabetico()
        test_desempate_mayor_edad()
        test_desempate_fecha_inscripcion()
        test_desempate_manual()
        test_servicio_desempate()
        test_persistencia()
        test_opciones_desempate()
        
        print("\n" + "=" * 60)
        print("✓ TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
        print("=" * 60)
    
    except AssertionError as e:
        print(f"\n✗ Error en prueba: {e}")
    except Exception as e:
        print(f"\n✗ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
